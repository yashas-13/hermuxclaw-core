const svg = d3.select("#graph-canvas");
const tooltip = d3.select("#tooltip");
const graphPanel = document.getElementById('graph-panel');

// D3 Simulation
let simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(graphPanel.clientWidth / 2, graphPanel.clientHeight / 2))
    .force("collision", d3.forceCollide().radius(40));

let nodeGroup = svg.append("g");
let linkGroup = svg.append("g");

svg.call(d3.zoom().on("zoom", (e) => {
    nodeGroup.attr("transform", e.transform);
    linkGroup.attr("transform", e.transform);
}));

async function fetchAPI(endpoint) {
    try { return await (await fetch(endpoint)).json(); } 
    catch { return null; }
}

async function updateDashboard() {
    const [graph, tasks, energy, swarm, alerts] = await Promise.all([
        fetchAPI('/graph'), fetchAPI('/tasks'), fetchAPI('/energy'),
        fetchAPI('/swarm'), fetchAPI('/alerts')
    ]);

    // Update Header Status
    const statusEl = document.getElementById('sys-status');
    const energyVal = energy ? energy.current : 0;
    const taskCount = tasks ? tasks.pending : 0;

    if (energyVal < 20) {
        statusEl.innerText = "CRITICAL";
        statusEl.className = "system-status status-critical";
    } else if (taskCount > 50) {
        statusEl.innerText = "DEGRADED";
        statusEl.className = "system-status status-degraded";
    } else {
        statusEl.innerText = "ACTIVE";
        statusEl.className = "system-status status-active";
    }

    document.getElementById('header-energy').innerText = `${energyVal}%`;
    document.getElementById('header-tasks').innerText = taskCount;
    document.getElementById('energy-fill').style.width = `${energyVal}%`;

    if (graph) renderGraph(graph);
    if (swarm) renderSwarm(swarm);
    if (tasks) renderTasks(tasks);
    if (alerts) renderAlerts(alerts);
}

function renderGraph(data) {
    const nodesMap = new Map();
    const links = [];

    Object.keys(data.calls).forEach(caller => {
        if (!nodesMap.has(caller)) nodesMap.set(caller, { id: caller });
        data.calls[caller].forEach(callee => {
            if (!nodesMap.has(callee)) nodesMap.set(callee, { id: callee });
            links.push({ source: caller, target: callee });
        });
    });

    const nodes = Array.from(nodesMap.values());
    
    const link = linkGroup.selectAll("line").data(links, d => d.source.id + "-" + d.target.id);
    link.exit().remove();
    const linkMerged = link.enter().append("line").style("stroke", "#333").style("stroke-width", 1.5).merge(link);

    const node = nodeGroup.selectAll("circle").data(nodes, d => d.id);
    node.exit().remove();
    const nodeEnter = node.enter().append("circle")
        .attr("r", 8)
        .style("fill", "#3b82f6")
        .style("stroke", "#000")
        .style("stroke-width", 2)
        .call(d3.drag()
            .on("start", (e,d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
            .on("drag", (e,d) => { d.fx = e.x; d.fy = e.y; })
            .on("end", (e,d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; })
        )
        .on("mouseover", (event, d) => {
            tooltip.transition().duration(100).style("opacity", 1);
            tooltip.html(d.id).style("left", (event.pageX + 10) + "px").style("top", (event.pageY - 20) + "px");
        })
        .on("mouseout", () => tooltip.transition().duration(300).style("opacity", 0));
        
    const nodeMerged = nodeEnter.merge(node);

    simulation.nodes(nodes).on("tick", () => {
        nodeMerged.attr("cx", d => d.x).attr("cy", d => d.y);
        linkMerged.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                  .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    });
    simulation.force("link").links(links);
    simulation.alpha(0.1).restart();
}

function renderSwarm(data) {
    document.getElementById('swarm-list').innerHTML = data.map(n => `
        <div class="list-item">
            <span>${n.node}</span>
            <span style="color:var(--state-active)">⚡${n.energy}% | 🧠${n.tasks}</span>
        </div>
    `).join('');
}

function renderTasks(data) {
    document.getElementById('task-list').innerHTML = `
        <div class="list-item"><span>PENDING</span><span class="tag queued">${data.pending}</span></div>
        <div class="list-item"><span>ACTIVE</span><span class="tag running">${data.active}</span></div>
        <div class="list-item"><span>COMPLETED</span><span class="tag done">${data.completed}</span></div>
    `;
}

function renderAlerts(data) {
    document.getElementById('alert-list').innerHTML = data.map(a => `
        <div class="alert-item ${a.level === 'INFO' ? 'info' : ''}">
            [${a.level}] ${a.msg}
        </div>
    `).join('');
}

setInterval(updateDashboard, 2000);
updateDashboard();
