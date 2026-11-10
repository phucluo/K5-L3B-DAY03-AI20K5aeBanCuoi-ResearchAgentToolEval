"""Interactive Neural Thought & Data Retrieval Visualizer for Research Agent.

Renders a futuristic Cyberpunk / Deep Navy HTML5 Canvas visualization showing:
- 360-degree radar sweep across the knowledge network.
- Neural thought nodes (Planner, Guardrail, Summarizer, arXiv, Policy, etc.).
- Animated data packets traveling along synapses.
- Dynamic glowing highlight on active tools called during the query.
"""
from __future__ import annotations

import json
from typing import Any


def render_thought_graph_html(
    active_tools: list[str] | None = None,
    status_text: str = "Hệ thống tri thức sẵn sàng",
    height: int = 420,
) -> str:
    """Generate self-contained HTML/JS string with animated Canvas."""
    active_tools = [t.lower() for t in (active_tools or [])]
    active_tools_json = json.dumps(active_tools)

    html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
  body {{
    background: transparent;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    overflow: hidden;
  }}
  .visualizer-container {{
    position: relative;
    width: 100%;
    height: {height}px;
    background: radial-gradient(circle at center, #0f172a 0%, #070913 85%, #03040a 100%);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.15) inset, 0 8px 30px rgba(0, 0, 0, 0.7);
    overflow: hidden;
  }}
  canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }}
  .hud-overlay {{
    position: absolute;
    top: 12px;
    left: 16px;
    z-index: 2;
    pointer-events: none;
    font-size: 11px;
    letter-spacing: 0.05em;
  }}
  .hud-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(30, 27, 75, 0.75);
    border: 1px solid rgba(129, 140, 248, 0.4);
    backdrop-filter: blur(8px);
    color: #c7d2fe;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
  }}
  .hud-pulse {{
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 1.8s infinite;
  }}
  @keyframes pulse {{
    0% {{ opacity: 0.4; transform: scale(0.9); }}
    50% {{ opacity: 1; transform: scale(1.3); }}
    100% {{ opacity: 0.4; transform: scale(0.9); }}
  }}
  .metrics-overlay {{
    position: absolute;
    bottom: 12px;
    right: 16px;
    z-index: 2;
    pointer-events: none;
    font-size: 11px;
    color: #94a3b8;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(99, 102, 241, 0.2);
    padding: 6px 12px;
    border-radius: 8px;
    backdrop-filter: blur(6px);
  }}
  .metrics-overlay span {{
    color: #818cf8;
    font-weight: 600;
  }}
  .legend-overlay {{
    position: absolute;
    bottom: 12px;
    left: 16px;
    z-index: 2;
    pointer-events: none;
    display: flex;
    gap: 12px;
    font-size: 10px;
    color: #94a3b8;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .legend-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }}
</style>
</head>
<body>
<div class="visualizer-container" id="container">
  <div class="hud-overlay">
    <div class="hud-badge">
      <div class="hud-pulse"></div>
      <span id="hud-status">COGNITIVE GRAPH: {status_text}</span>
    </div>
  </div>
  <div class="metrics-overlay">
    SCANNER: <span>ONLINE</span> | ACTIVE NODES: <span id="active-count">0</span> | PROTOCOL: <span>NEURAL-v3</span>
  </div>
  <div class="legend-overlay">
    <div class="legend-item"><div class="legend-dot" style="background:#6366f1;box-shadow:0 0 6px #6366f1"></div><span>Bộ suy luận / Planner</span></div>
    <div class="legend-item"><div class="legend-dot" style="background:#10b981;box-shadow:0 0 6px #10b981"></div><span>Công cụ kích hoạt (Fired)</span></div>
    <div class="legend-item"><div class="legend-dot" style="background:#38bdf8;box-shadow:0 0 6px #38bdf8"></div><span>Dòng gói tin (Data Stream)</span></div>
  </div>
  <canvas id="graphCanvas"></canvas>
</div>

<script>
(function() {{
  const canvas = document.getElementById('graphCanvas');
  const ctx = canvas.getContext('2d');
  const container = document.getElementById('container');
  const activeTools = {active_tools_json};

  let width = container.clientWidth || 800;
  let height = container.clientHeight || {height};
  canvas.width = width * window.devicePixelRatio;
  canvas.height = height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  // Nodes definition
  const centerX = width * 0.5;
  const centerY = height * 0.52;

  const nodes = [
    {{ id: 'query', label: 'User Intent', sub: 'Input Query', x: width * 0.12, y: centerY, type: 'core', active: true }},
    {{ id: 'planner', label: 'Agent Brain', sub: 'Chain-of-Thought', x: width * 0.32, y: centerY, type: 'brain', active: true }},
    {{ id: 'guardrail', label: 'Guardrail Gate', sub: 'clarify / safety', x: width * 0.32, y: centerY - 90, type: 'guard', active: activeTools.includes('clarify') }},
    
    // Tools cluster
    {{ id: 'summarize_paper', label: 'summarize_paper', sub: 'CP3 Custom Tool', x: width * 0.62, y: centerY - 110, type: 'tool', active: activeTools.includes('summarize_paper') }},
    {{ id: 'papers', label: 'papers (arXiv)', sub: 'Open Academic API', x: width * 0.70, y: centerY - 40, type: 'tool', active: activeTools.includes('papers') || activeTools.includes('arxiv_search') }},
    {{ id: 'policy', label: 'company_policy', sub: 'Local Doc Retrieval', x: width * 0.70, y: centerY + 50, type: 'tool', active: activeTools.includes('policy') || activeTools.includes('search_company_policy') }},
    {{ id: 'web', label: 'web / timeline', sub: 'Social & Search', x: width * 0.62, y: centerY + 120, type: 'tool', active: activeTools.includes('timeline') || activeTools.includes('lookup') }},

    // Output & Dispatch
    {{ id: 'format', label: 'format_digest', sub: 'Synthesis Engine', x: width * 0.88, y: centerY - 30, type: 'tool', active: activeTools.includes('format') || activeTools.includes('format_digest') }},
    {{ id: 'output', label: 'Executive Report', sub: 'Final Response', x: width * 0.88, y: centerY + 60, type: 'core', active: true }}
  ];

  // Edges definition
  const edges = [
    {{ from: 'query', to: 'planner' }},
    {{ from: 'planner', to: 'guardrail' }},
    {{ from: 'planner', to: 'summarize_paper' }},
    {{ from: 'planner', to: 'papers' }},
    {{ from: 'planner', to: 'policy' }},
    {{ from: 'planner', to: 'web' }},
    {{ from: 'summarize_paper', to: 'format' }},
    {{ from: 'papers', to: 'format' }},
    {{ from: 'policy', to: 'format' }},
    {{ from: 'web', to: 'format' }},
    {{ from: 'format', to: 'output' }},
    {{ from: 'guardrail', to: 'output' }}
  ];

  // Update active count HUD
  const activeCountEl = document.getElementById('active-count');
  if (activeCountEl) {{
    const count = nodes.filter(n => n.active && n.type === 'tool').length;
    activeCountEl.innerText = count > 0 ? count + ' (Fired)' : 'Standby';
  }}

  // Data packets flowing on edges
  const packets = [];
  edges.forEach((edge, idx) => {{
    const fromNode = nodes.find(n => n.id === edge.from);
    const toNode = nodes.find(n => n.id === edge.to);
    const isActive = fromNode.active && toNode.active;
    const packetCount = isActive ? 2 : 1;
    for (let i = 0; i < packetCount; i++) {{
      packets.push({{
        from: fromNode,
        to: toNode,
        progress: (i / packetCount) + (Math.random() * 0.2),
        speed: 0.006 + Math.random() * 0.004,
        active: isActive
      }});
    }}
  }});

  // Radar beam state
  let radarAngle = 0;

  function draw() {{
    ctx.clearRect(0, 0, width, height);

    // 1. Draw radar sweep cone
    ctx.save();
    ctx.translate(centerX, centerY);
    const radarRadius = Math.max(width, height) * 0.65;
    const gradient = ctx.createRadialGradient(0, 0, 10, 0, 0, radarRadius);
    gradient.addColorStop(0, 'rgba(99, 102, 241, 0.12)');
    gradient.addColorStop(0.5, 'rgba(56, 189, 248, 0.04)');
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, radarRadius, radarAngle, radarAngle + 0.35);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();

    // Radar beam line
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(Math.cos(radarAngle + 0.35) * radarRadius, Math.sin(radarAngle + 0.35) * radarRadius);
    ctx.strokeStyle = 'rgba(129, 140, 248, 0.35)';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();

    radarAngle += 0.015;
    if (radarAngle > Math.PI * 2) radarAngle -= Math.PI * 2;

    // 2. Draw subtle grid background
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.05)';
    ctx.lineWidth = 1;
    for (let x = 0; x < width; x += 40) {{
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
    }}
    for (let y = 0; y < height; y += 40) {{
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
    }}

    // 3. Draw edges
    edges.forEach(edge => {{
      const fn = nodes.find(n => n.id === edge.from);
      const tn = nodes.find(n => n.id === edge.to);
      const isHighlit = fn.active && tn.active;

      ctx.beginPath();
      ctx.moveTo(fn.x, fn.y);
      ctx.lineTo(tn.x, tn.y);
      ctx.strokeStyle = isHighlit ? 'rgba(99, 102, 241, 0.65)' : 'rgba(51, 65, 85, 0.35)';
      ctx.lineWidth = isHighlit ? 2 : 1;
      if (isHighlit) {{
        ctx.shadowColor = '#6366f1';
        ctx.shadowBlur = 8;
      }}
      ctx.stroke();
      ctx.shadowBlur = 0;
    }});

    // 4. Update and draw data packets
    packets.forEach(p => {{
      p.progress += p.speed;
      if (p.progress > 1) p.progress = 0;

      const px = p.from.x + (p.to.x - p.from.x) * p.progress;
      const py = p.from.y + (p.to.y - p.from.y) * p.progress;

      ctx.beginPath();
      ctx.arc(px, py, p.active ? 3.5 : 2, 0, Math.PI * 2);
      ctx.fillStyle = p.active ? '#38bdf8' : 'rgba(148, 163, 184, 0.5)';
      if (p.active) {{
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 10;
      }}
      ctx.fill();
      ctx.shadowBlur = 0;
    }});

    // 5. Draw nodes
    nodes.forEach(node => {{
      const isFired = node.active && (node.type === 'tool' || node.id === 'guardrail');

      // Outer glow ring if active/fired
      if (isFired) {{
        ctx.beginPath();
        const pulse = 18 + Math.sin(Date.now() * 0.005) * 4;
        ctx.arc(node.x, node.y, pulse, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.5)';
        ctx.lineWidth = 1.5;
        ctx.shadowColor = '#10b981';
        ctx.shadowBlur = 12;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }} else if (node.type === 'brain') {{
        ctx.beginPath();
        const pulse = 22 + Math.sin(Date.now() * 0.004) * 3;
        ctx.arc(node.x, node.y, pulse, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(99, 102, 241, 0.6)';
        ctx.lineWidth = 2;
        ctx.shadowColor = '#6366f1';
        ctx.shadowBlur = 14;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }}

      // Node base circle
      ctx.beginPath();
      let nodeRadius = 12;
      let fillColor = '#1e293b';
      let strokeColor = '#475569';

      if (node.type === 'brain') {{
        nodeRadius = 16;
        fillColor = '#312e81';
        strokeColor = '#818cf8';
      }} else if (isFired) {{
        nodeRadius = 13;
        fillColor = '#064e3b';
        strokeColor = '#10b981';
      }} else if (node.type === 'guard') {{
        fillColor = '#701a75';
        strokeColor = '#d946ef';
      }} else if (node.type === 'core') {{
        fillColor = '#0f172a';
        strokeColor = '#60a5fa';
      }}

      ctx.arc(node.x, node.y, nodeRadius, 0, Math.PI * 2);
      ctx.fillStyle = fillColor;
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = strokeColor;
      ctx.stroke();

      // Node labels
      ctx.font = 'bold 11px -apple-system, BlinkMacSystemFont, monospace';
      ctx.fillStyle = isFired ? '#a7f3d0' : (node.type === 'brain' ? '#c7d2fe' : '#e2e8f0');
      ctx.textAlign = 'center';
      ctx.fillText(node.label, node.x, node.y - nodeRadius - 6);

      ctx.font = '9px -apple-system, BlinkMacSystemFont, sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.fillText(node.sub, node.x, node.y + nodeRadius + 14);
    }});

    requestAnimationFrame(draw);
  }}

  draw();

  window.addEventListener('resize', () => {{
    width = container.clientWidth || 800;
    height = container.clientHeight || {height};
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }});
}})();
</script>
</body>
</html>
    """
    return html
