
/**
 * CobolScope Interactive Call Graph Viewer Runtime Engine
 * Encapsulated client runtime for Cytoscape, ELK, Dagre, Inspector, and Code Viewer.
 */
(function(window, document) {
  'use strict';

  // Safe iframe detection (no cross-origin exceptions)
  try {
    if (window.self !== window.top) {
      document.documentElement.classList.add("in-portal-iframe");
    }
  } catch (e) {
    document.documentElement.classList.add("in-portal-iframe");
  }

  // Escape HTML helper (preserves quotes for code viewing parity)
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }
  window.escapeHtml = escapeHtml;

  // Module-level shared variables accessible to all components
  let graphData = {};
  let cytoElements = [];
  let canonicalElements = [];
  let clonedElements = [];
  let initialEnableCloning = false;
  let layoutHeuristics = {};
  let initialEnginePreference = "cytoscape";
  let sourceCodeRaw = "";

  let currentEngine = "cytoscape";
  let selectedRoutineNode = null;
  let cy = null;
  let cyLevel3 = null;
  let cyContainer = null;
  let layoutSelect = null;
  let cytoLayoutGroup = null;

  // Pre-populate data from #cobolscope-data if already in DOM
  function populateDataIsland() {
    const dataEl = document.getElementById("cobolscope-data");
    if (!dataEl) return false;
    try {
      const payload = JSON.parse(dataEl.textContent);
      graphData = payload.graph || {};
      cytoElements = payload.cytoElements || [];
      canonicalElements = payload.canonicalElements || [];
      clonedElements = payload.clonedElements || [];
      initialEnableCloning = !!payload.initialEnableCloning;
      layoutHeuristics = payload.layoutHeuristics || {};
      initialEnginePreference = payload.initialEnginePreference || "cytoscape";
      sourceCodeRaw = payload.sourceCodeRaw || "";

      currentEngine = initialEnginePreference;
      selectedRoutineNode = null;
      cyContainer = document.getElementById("cy-container");
      layoutSelect = document.getElementById("layoutSelect");
      cytoLayoutGroup = document.getElementById("cytoLayoutGroup");

      // Expose to window for backward compatibility and debugging
      window.graphData = graphData;
      window.cytoElements = cytoElements;
      window.canonicalElements = canonicalElements;
      window.clonedElements = clonedElements;
      window.sourceCodeRaw = sourceCodeRaw;
      window.selectedRoutineNode = selectedRoutineNode;
      window.cyContainer = cyContainer;
      window.layoutSelect = layoutSelect;
      window.cytoLayoutGroup = cytoLayoutGroup;
      return true;
    } catch(e) {
      console.error("[CobolScope] Failed to parse JSON data island:", e);
      return false;
    }
  }

  // Populate data island immediately if elements exist
  populateDataIsland();


/* --- diagnostics.js.j2 --- */

// Diagnostic Telemetry & Error Handling Subsystem
    const CobolScopeLog = {
      info: (msg, ...args) => console.log(`[CobolScope] ${msg}`, ...args),
      warn: (msg, ...args) => console.warn(`[CobolScope WARN] ${msg}`, ...args),
      error: (msg, ...args) => {
        console.error(`[CobolScope ERROR] ${msg}`, ...args);
        CobolScopeLog.showOnScreenError(msg);
      },
      showOnScreenError: (msg) => {
        if (!document.body) {
          console.error("[CobolScope Early Error]", msg);
          return;
        }
        let errBox = document.getElementById("cobolscopeErrorBanner");
        if (!errBox) {
          errBox = document.createElement("div");
          errBox.id = "cobolscopeErrorBanner";
          errBox.style.position = "fixed";
          errBox.style.bottom = "20px";
          errBox.style.left = "20px";
          errBox.style.maxWidth = "520px";
          errBox.style.background = "#FEF2F2";
          errBox.style.border = "1px solid #DC2626";
          errBox.style.borderRadius = "8px";
          errBox.style.padding = "12px 16px";
          errBox.style.color = "#991B1B";
          errBox.style.fontSize = "0.85rem";
          errBox.style.boxShadow = "0 10px 15px -3px rgba(0,0,0,0.15)";
          errBox.style.zIndex = "999999";
          document.body.appendChild(errBox);
        }
        errBox.innerHTML = `<strong>CobolScope Error:</strong> ${escapeHtml(msg)}<br><small style="color:#B91C1C;">Check browser console for details.</small>`;
      }
    };

    window.addEventListener("error", (e) => {
      if (e.message && e.message.includes("Script error")) return;
      CobolScopeLog.error(`Uncaught script error: ${e.message} at ${e.filename || 'script'}:${e.lineno}`);
    });


/* --- cyto_call_graph.js.j2 --- */

// Cytoscape Call Graph Engine & Styling
    function initCytoscape() {
      CobolScopeLog.info("Initializing Cytoscape Level 2 Call Graph...");
      if (typeof cytoscape === "undefined") {
        CobolScopeLog.error("Cytoscape.js could not be loaded.");
        return;
      }

      if (typeof cytoscapeDagre !== "undefined") {
        cytoscape.use(cytoscapeDagre);
      }
      if (typeof cytoscapeElk !== "undefined") {
        cytoscape.use(cytoscapeElk);
      } else if (typeof window !== "undefined" && typeof window.cytoscapeElk !== "undefined") {
        cytoscape.use(window.cytoscapeElk);
      }

      try {
        cy = cytoscape({
          container: cyContainer,
          elements: cytoElements,
          boxSelectionEnabled: false,
          autounselectify: false,
          style: [
            // Parent Cluster Nodes
            {
              selector: "node.cluster-node",
              style: {
                "label": "data(label)",
                "text-valign": "top",
                "text-halign": "center",
                "text-margin-y": 8,
                "font-family": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
                "font-size": 13,
                "font-weight": "bold",
                "color": "data(text_color)",
                "background-color": "data(fill_color)",
                "background-opacity": 0.45,
                "border-width": 2,
                "border-color": "data(color)",
                "border-opacity": 0.8,
                "shape": "round-rectangle",
                "padding": 18,
                "z-index": 1
              }
            },
            // Child Routine Nodes
            {
              selector: "node.routine-node",
              style: {
                "label": function(ele) {
                  const d = ele.data();
                  let lines = [];
                  if (d.is_clone) {
                    const totalStr = d.clone_total > 1 ? "/" + d.clone_total : "";
                    lines.push(d.label + " [CLONE " + d.clone_index + totalStr + "]");
                  } else {
                    lines.push(d.label);
                  }
                  if (d.type_label) {
                    lines.push("[" + d.type_label + "]");
                  }
                  lines.push(d.lines + " | CC:" + d.cyclomatic_complexity);
                  if (d.io_badge) {
                    lines.push(d.io_badge);
                  }
                  return lines.join("\n");
                },
                "text-wrap": "wrap",
                "text-valign": "center",
                "text-halign": "center",
                "font-family": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
                "font-size": 11,
                "font-weight": "600",
                "color": "#0F172A",
                "background-color": "#FFFFFF",
                "border-width": 2.5,
                "border-color": "data(color)",
                "shape": "round-rectangle",
                "width": "label",
                "height": "label",
                "padding": 16,
                "z-index": 10
              }
            },
            // Cloned Utility Nodes
            {
              selector: "node.clone-node",
              style: {
                "border-style": "dashed",
                "border-width": 2.5,
                "background-opacity": 0.88,
                "opacity": 0.92
              }
            },

            // Subsystem Visual Tinting
            {
              selector: "node.type-file_io",
              style: { "border-color": "#107C41", "background-color": "#F2F9F4" }
            },
            {
              selector: "node.type-database_io",
              style: { "border-color": "#008272", "background-color": "#F0FDFB" }
            },
            {
              selector: "node.type-business_logic",
              style: { "border-color": "#0056B3", "background-color": "#EBF3FC" }
            },
            {
              selector: "node.type-initialization",
              style: { "border-color": "#2C5282", "background-color": "#EBF8FF" }
            },
            {
              selector: "node.type-error_handling",
              style: { "border-color": "#DC2626", "background-color": "#FEF2F2" }
            },
            {
              selector: "node.type-termination",
              style: { "border-color": "#4A5568", "background-color": "#F4F6F8" }
            },
            // Entry Point Routine
            {
              selector: "node.entry-point",
              style: {
                "border-width": 3.5,
                "border-color": "#0056B3",
                "background-color": "#EBF3FC",
                "color": "#003875"
              }
            },
            // Terminal Routines (STOP RUN, GOBACK)
            {
              selector: "node.terminal-node",
              style: {
                "border-width": 3,
                "border-color": "#4A5568",
                "background-color": "#F4F6F8",
                "color": "#1A202C"
              }
            },
            // Error Handling & Abend Routines
            {
              selector: "node.type-error_handling",
              style: {
                "border-width": 3.5,
                "border-color": "#DC2626",
                "background-color": "#FEF2F2",
                "color": "#991B1B"
              }
            },
            // Selection & Highlights
            {
              selector: "node.routine-node:selected",
              style: {
                "border-width": 4,
                "border-color": "#F59E0B",
                "shadow-blur": 14,
                "shadow-color": "rgba(245, 158, 11, 0.45)",
                "opacity": 1.0,
                "z-index": 50
              }
            },
            {
              selector: "node.routine-node.neighbor-highlight",
              style: {
                "opacity": 1.0,
                "z-index": 40
              }
            },
            {
              selector: "edge.neighbor-highlight",
              style: {
                "opacity": 1.0,
                "width": 3,
                "line-color": "#0056B3",
                "target-arrow-color": "#0056B3",
                "z-index": 35
              }
            },
            {
              selector: "node.routine-node.dimmed",
              style: {
                "opacity": 0.2
              }
            },
            {
              selector: "edge.dimmed",
              style: {
                "opacity": 0.12
              }
            },
            {
              selector: "node.routine-node:selected.dimmed, node.routine-node.neighbor-highlight.dimmed",
              style: {
                "opacity": 1.0
              }
            },
            // Invocations (Edges)
            {
              selector: "edge.call-edge",
              style: {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "target-arrow-color": "#94A3B8",
                "line-color": "#CBD5E1",
                "width": 2,
                "arrow-scale": 1.2,
                "opacity": 0.85,
                "label": "data(label)",
                "font-size": 9,
                "color": "#64748B",
                "text-background-color": "#FFFFFF",
                "text-background-opacity": 0.8,
                "text-background-padding": 2
              }
            },
            {
              selector: "edge.edge-fallthrough",
              style: {
                "line-style": "dashed",
                "line-color": "#94A3B8",
                "target-arrow-color": "#94A3B8",
                "width": 1.5,
                "opacity": 0.6
              }
            },
            {
              selector: "edge.error-branch",
              style: {
                "line-color": "#DC2626",
                "target-arrow-color": "#DC2626",
                "line-style": "dashed",
                "width": 2.5,
                "opacity": 0.95
              }
            }
          ]
        });

        const initialLayout = layoutSelect ? layoutSelect.value : "dagre";
        applyCytoLayout(initialLayout);

        cy.on("tap", "node.routine-node", (evt) => {
          const node = evt.target;
          const origName = node.data("original_name") || node.data("name") || node.data("label");
          highlightCytoNeighbors(node);
          selectNode(origName);
        });

        cy.on("dbltap", "node.routine-node", (evt) => {
          const node = evt.target;
          const origName = node.data("original_name") || node.data("name") || node.data("label");
          const routine = graphData.nodes[origName] || graphData.nodes[node.data("name")];
          if (routine) {
            selectNode(origName);
            openRoutineFlowModal(routine);
          }
        });

        cy.on("tap", (evt) => {
          if (evt.target === cy) {
            clearHighlight();
          }
        });

        CobolScopeLog.info("Cytoscape Level 2 initialized successfully.");
      } catch (err) {
        CobolScopeLog.error(`Cytoscape initialization failed: ${err.message}`);
      }
    }

    function applyCytoLayout(layoutName) {
      if (!cy) return;
      CobolScopeLog.info(`Applying Cytoscape layout: ${layoutName}`);

      const nSep = (typeof layoutHeuristics !== "undefined" && layoutHeuristics && layoutHeuristics.cyto_nodesep) ? layoutHeuristics.cyto_nodesep : 50;
      const rSep = (typeof layoutHeuristics !== "undefined" && layoutHeuristics && layoutHeuristics.cyto_ranksep) ? layoutHeuristics.cyto_ranksep : 60;
      const rankerAlg = (typeof layoutHeuristics !== "undefined" && layoutHeuristics && layoutHeuristics.ranker) ? layoutHeuristics.ranker : "network-simplex";

      let layoutConfig = { name: layoutName, padding: 40 };
      if (layoutName === "dagre") {
        layoutConfig = {
          name: "dagre",
          rankDir: "TB",
          nodeSep: nSep,
          rankSep: rSep,
          ranker: rankerAlg,
          padding: 40,
          animate: true,
          animationDuration: 300
        };
      } else if (layoutName === "elk-layered" || layoutName === "elk") {
        layoutConfig = {
          name: "elk",
          elk: {
            "algorithm": "layered",
            "elk.direction": "DOWN",
            "elk.spacing.nodeNodeBetweenLayers": rSep,
            "elk.spacing.nodeNode": nSep,
            "elk.layered.crossingMinimization.strategy": "LAYER_SWEEP",
            "elk.layered.nodePlacement.strategy": "BRANDES_KOEPF",
            "elk.layered.cycleBreaking.strategy": "GREEDY",
            "elk.layered.spacing.edgeEdgeBetweenLayers": 12,
            "elk.edgeRouting": "ORTHOGONAL"
          },
          padding: 40,
          animate: true,
          animationDuration: 350
        };
      } else if (layoutName === "breadthfirst") {
        layoutConfig = {
          name: "breadthfirst",
          directed: true,
          padding: 40,
          spacingFactor: 1.25,
          animate: true
        };
      } else if (layoutName === "cose") {
        layoutConfig = {
          name: "cose",
          idealEdgeLength: 100,
          nodeOverlap: 20,
          refresh: 20,
          fit: true,
          padding: 40,
          randomize: false,
          componentSpacing: 100,
          nodeRepulsion: 400000,
          edgeElasticity: 100,
          nestingFactor: 5,
          gravity: 80,
          numIter: 1000,
          initialTemp: 200,
          coolingFactor: 0.95,
          minTemp: 1.0,
          animate: true
        };
      }

      try {
        cy.layout(layoutConfig).run();
      } catch (err) {
        CobolScopeLog.warn(`Layout '${layoutName}' failed: ${err.message}. Falling back to 'dagre'.`);
        if (layoutName !== "dagre") {
          applyCytoLayout("dagre");
        }
      }
    }

    const activeLayoutSelect = typeof layoutSelect !== "undefined" ? layoutSelect : document.getElementById("layoutSelect");
    if (activeLayoutSelect) {
      activeLayoutSelect.addEventListener("change", (e) => {
        applyCytoLayout(e.target.value);
      });
    }

    const toggleCloneUtilities = document.getElementById("toggleCloneUtilities");
    if (toggleCloneUtilities) {
      toggleCloneUtilities.addEventListener("change", (e) => {
        const useClones = e.target.checked;
        CobolScopeLog.info(`Toggling Disentangle Utilities: ${useClones}`);
        if (!cy) return;

        const targetElements = useClones ? clonedElements : canonicalElements;
        if (!targetElements || targetElements.length === 0) return;

        cy.batch(() => {
          cy.elements().remove();
          cy.add(targetElements);
        });

        const activeLayout = activeLayoutSelect ? activeLayoutSelect.value : "dagre";
        applyCytoLayout(activeLayout);
      });
    }

    function highlightCytoNeighbors(node) {
      if (!cy) return;
      cy.elements().removeClass("dimmed neighbor-highlight");

      const connectedEdges = node.connectedEdges();
      const neighborNodes = connectedEdges.connectedNodes(".routine-node");
      let focalNodes = neighborNodes.union(node);

      // If clicked node is a clone or has clones, highlight sister clones too
      const isClone = node.data("is_clone");
      const origName = node.data("original_name") || node.data("name") || node.data("label");
      if (isClone || (origName && (clonedElements || []).length > 0)) {
        const sisters = cy.nodes(".routine-node").filter(n => {
          const nOrig = n.data("original_name") || n.data("name") || n.data("label");
          return nOrig && nOrig.toUpperCase() === origName.toUpperCase();
        });
        focalNodes = focalNodes.union(sisters);
      }

      // Add highlight to focal routines and their connecting edges
      focalNodes.addClass("neighbor-highlight");
      connectedEdges.addClass("neighbor-highlight");

      // Mark the clicked node as selected
      cy.nodes().unselect();
      node.select();

      // Only dim other routine nodes and other edges
      // NEVER dim cluster nodes (compound parents), as parent opacity dims children in Cytoscape
      const otherRoutines = cy.nodes(".routine-node").difference(focalNodes);
      const otherEdges = cy.edges().difference(connectedEdges);

      otherRoutines.addClass("dimmed");
      otherEdges.addClass("dimmed");
    }

    function focusNode(nodeName) {
      if (!cy) return;
      const cyNode = cy.nodes(".routine-node").filter(n => {
        const nName = (n.data("name") || n.data("label") || "").toUpperCase();
        const origName = (n.data("original_name") || "").toUpperCase();
        const target = nodeName.toUpperCase();
        return nName === target || origName === target;
      });
      if (cyNode.length > 0) {
        highlightCytoNeighbors(cyNode[0]);
        cy.animate({
          center: { eles: cyNode[0] },
          zoom: Math.max(cy.zoom(), 1.1),
          duration: 400
        });
      }
    }



/* --- linear_card.js.j2 --- */

// Procedure Action Card & Enhanced Linear Summary Card Renderer
function renderCfgInspectorSection(node) {
  const secEl = document.getElementById("inspCfgSection");
  if (!secEl) return;
  secEl.innerHTML = "";

  const btnFlow = document.getElementById("btnOpenFlowchart") || document.getElementById("btnOpenLevel3");
  const btnFlowText = document.getElementById("btnOpenFlowchartText");

  if (node.is_cfg_eligible) {
    // --- Branching Routine (CC > 1): Connect to Logic Flowchart Action ---
    if (btnFlow) {
      btnFlow.disabled = false;
      if (btnFlowText) btnFlowText.textContent = "Logic Flowchart";
      btnFlow.onclick = () => openLevel3Modal(node);
      btnFlow.title = "View procedure logic flowchart";
    }
    secEl.innerHTML = "";
  } else {
    // --- Linear Routine: Connect to Statement Trace Action & Show Clean Inline Trace ---
    if (btnFlow) {
      btnFlow.disabled = false;
      if (btnFlowText) btnFlowText.textContent = "Statement Trace";
      btnFlow.onclick = () => openLinearCardModal(node);
      btnFlow.title = "View sequential execution statement trace";
    }

    const stmts = node.cfg_linear_statements || [];
    if (stmts.length > 0) {
      const sectionDiv = document.createElement("div");
      sectionDiv.className = "inspector-section";
      sectionDiv.style.marginTop = "14px";

      const sectionTitle = document.createElement("div");
      sectionTitle.className = "section-title";
      sectionTitle.textContent = `Sequential Statements (${stmts.length})`;
      sectionDiv.appendChild(sectionTitle);

      // Verb Category Distribution Pills
      const verbCounts = {};
      stmts.forEach(s => {
        const v = s.verb || "STATEMENT";
        verbCounts[v] = (verbCounts[v] || 0) + 1;
      });

      const pillsContainer = document.createElement("div");
      pillsContainer.style.display = "flex";
      pillsContainer.style.flexWrap = "wrap";
      pillsContainer.style.gap = "4px";
      pillsContainer.style.marginBottom = "8px";

      Object.entries(verbCounts).forEach(([verb, count]) => {
        const pill = document.createElement("span");
        pill.style.fontSize = "0.68rem";
        pill.style.fontWeight = "600";
        pill.style.padding = "2px 6px";
        pill.style.borderRadius = "3px";
        pill.style.background = "var(--bg-primary)";
        pill.style.color = "var(--text-secondary)";
        pill.style.border = "1px solid var(--border-color)";
        pill.textContent = `${verb} (${count})`;
        pillsContainer.appendChild(pill);
      });
      sectionDiv.appendChild(pillsContainer);

      // Formatted Interactive Statement Trace
      const traceBox = document.createElement("div");
      traceBox.style.background = "var(--bg-primary)";
      traceBox.style.border = "1px solid var(--border-color)";
      traceBox.style.borderRadius = "4px";
      traceBox.style.padding = "6px";
      traceBox.style.maxHeight = "180px";
      traceBox.style.overflowY = "auto";
      traceBox.style.fontFamily = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
      traceBox.style.fontSize = "0.72rem";

      stmts.forEach((s, idx) => {
        const row = document.createElement("div");
        row.style.display = "flex";
        row.style.alignItems = "flex-start";
        row.style.gap = "6px";
        row.style.padding = "3px 4px";
        row.style.borderRadius = "3px";
        if (idx % 2 === 0) row.style.background = "#FFFFFF";

        const lineSpan = document.createElement("span");
        lineSpan.style.color = "var(--text-muted)";
        lineSpan.style.minWidth = "34px";
        lineSpan.style.fontSize = "0.68rem";
        lineSpan.textContent = s.line ? `L${s.line}` : "L--";

        const verbSpan = document.createElement("span");
        verbSpan.style.fontWeight = "700";
        verbSpan.style.fontSize = "0.68rem";
        verbSpan.style.padding = "1px 4px";
        verbSpan.style.borderRadius = "3px";

        if (s.category === "data") {
          verbSpan.style.background = "#F0F4F8";
          verbSpan.style.color = "#245882";
        } else if (s.category === "call") {
          verbSpan.style.background = "#EBF3FC";
          verbSpan.style.color = "#0056B3";
        } else if (s.category === "io") {
          verbSpan.style.background = "#E8F5E9";
          verbSpan.style.color = "#198754";
        } else if (s.category === "terminal") {
          verbSpan.style.background = "#FDE8E8";
          verbSpan.style.color = "#C82333";
        } else {
          verbSpan.style.background = "#ECEFF2";
          verbSpan.style.color = "#4A5568";
        }
        verbSpan.textContent = s.verb || "STMT";

        const textSpan = document.createElement("span");
        textSpan.style.flex = "1";
        textSpan.style.wordBreak = "break-word";
        textSpan.style.color = "#1E293B";

        if ((s.category === "call" || s.category === "terminal") && s.target && graphData.nodes[s.target.toUpperCase()]) {
          textSpan.innerHTML = `${escapeHtml(s.text.replace(s.target, ""))} <a href="#" style="color:var(--primary); font-weight:700; text-decoration:underline;">${escapeHtml(s.target)}</a>`;
          const a = textSpan.querySelector("a");
          if (a) {
            a.onclick = (e) => {
              e.preventDefault();
              selectNode(s.target);
              focusNode(s.target);
            };
          }
        } else {
          textSpan.textContent = s.text;
        }

        row.appendChild(lineSpan);
        row.appendChild(verbSpan);
        row.appendChild(textSpan);
        traceBox.appendChild(row);
      });

      sectionDiv.appendChild(traceBox);
      secEl.appendChild(sectionDiv);
    }
  }
}


/* --- inspector.js.j2 --- */

// Node Inspector & Enhanced Linear Summary Card
    function selectNode(nodeName) {
      if (!nodeName) return;
      const lookupKey = nodeName.toUpperCase().trim();
      let node = graphData.nodes[lookupKey];
      if (!node) {
        for (const k in graphData.nodes) {
          const candidate = graphData.nodes[k];
          if ((candidate.original_name && candidate.original_name.toUpperCase().trim() === lookupKey) ||
              (candidate.name && candidate.name.toUpperCase().trim() === lookupKey)) {
            node = candidate;
            break;
          }
        }
      }
      if (!node) return;


      selectedRoutineNode = node;

      const inspectorEl = document.getElementById("inspector");
      if (inspectorEl && inspectorEl.style.display === "none") {
        if (typeof toggleInspector === "function") {
          toggleInspector(true);
        } else {
          inspectorEl.style.display = "flex";
        }
      }

      // Update Header: Routine Name spans across full panel
      document.getElementById("inspTitle").textContent = node.name || "Routine";

      // Subtitle / Section context
      const subtitleEl = document.getElementById("inspSubtitle");
      if (subtitleEl) {
        subtitleEl.textContent = node.section ? `Section: ${node.section}` : "";
      }

      // Entry Point Badge
      const entryBadge = document.getElementById("inspEntryBadge");
      if (entryBadge) {
        entryBadge.style.display = node.is_entry_point ? "inline-flex" : "none";
      }

      // Routine Type Badge (human-friendly title instead of raw SCREAMING_SNAKE_CASE)
      const typeBadge = document.getElementById("inspTypeBadge");
      if (typeBadge) {
        const typeLabels = {
          "MAIN_DRIVER": "Main Driver",
          "BUSINESS_LOGIC": "Business Logic",
          "FILE_IO": "File I/O",
          "DB_SUBSYSTEM": "DB / Subsystem",
          "TABLE_LOOKUP": "Table Lookup",
          "ERROR_HANDLING": "Error Handling",
          "ROUTINE_EXIT": "Exit Routine",
          "GENERIC": "Procedure"
        };
        typeBadge.textContent = typeLabels[node.node_type] || node.node_type || "Procedure";
      }

      document.getElementById("inspSection").textContent = node.section ? node.section : "—";
      document.getElementById("inspPara").textContent = node.name;
      document.getElementById("inspLines").textContent = node.start_line > 0 ? `L${node.start_line}-${node.end_line}` : "N/A";
      document.getElementById("inspCC").textContent = node.cyclomatic_complexity;
      document.getElementById("inspStmts").textContent = node.statement_count;
      document.getElementById("inspCluster").textContent = node.cluster_id.replace("cluster_", "");

      const btnViewCode = document.getElementById("btnViewRoutineCode");
      const btnViewCodeText = document.getElementById("btnViewRoutineCodeText") || (btnViewCode ? btnViewCode.querySelector("span") : null);
      if (btnViewCode && btnViewCodeText) {
        if (node.start_line > 0) {
          btnViewCode.disabled = false;
          const mainFile = (typeof graphData !== "undefined" && graphData.source_file) ? graphData.source_file : "";
          const isCopybook = Boolean(node.source_file && mainFile && !mainFile.endsWith(node.source_file) && !node.source_file.endsWith(mainFile));
          const lineSpan = isCopybook ? `${node.source_file}:L${node.start_line}` : `L${node.start_line}–L${node.end_line}`;
          btnViewCodeText.textContent = "Source Code";
          btnViewCode.title = `View source code (${lineSpan})`;
        } else {
          btnViewCode.disabled = true;
          btnViewCodeText.textContent = "Source Code";
          btnViewCode.title = "Line info unavailable";
        }
      }

      if (typeof highlightRoutineInCode === "function") {
        highlightRoutineInCode(node.start_line, node.end_line, node.name, node.source_file);
      }

      // Render Logic Flowchart / Linear Summary Card
      renderCfgInspectorSection(node);

      // Callers List
      const callersEl = document.getElementById("inspCallers");
      callersEl.innerHTML = "";
      if (node.called_by.length > 0) {
        node.called_by.forEach(caller => {
          const tag = document.createElement("span");
          tag.className = "tag";
          tag.textContent = caller;
          tag.onclick = () => { selectNode(caller); focusNode(caller); };
          callersEl.appendChild(tag);
        });
      } else {
        callersEl.innerHTML = '<span style="font-size:0.8rem; color:var(--text-muted);">' + (node.is_entry_point ? '<span style="color:var(--primary); font-weight:600;">[Entry Point]</span> Program Entry' : 'Root / Uncalled') + '</span>';
      }

      // Successors List
      const succEl = document.getElementById("inspSuccessors");
      succEl.innerHTML = "";
      if (node.successors.length > 0) {
        node.successors.forEach(succ => {
          const tag = document.createElement("span");
          tag.className = "tag";
          tag.textContent = succ;
          tag.onclick = () => { selectNode(succ); focusNode(succ); };
          succEl.appendChild(tag);
        });
      } else {
        succEl.innerHTML = '<span style="font-size:0.8rem; color:var(--text-muted);">Terminal / None</span>';
      }

      // Read Fields
      const readEl = document.getElementById("inspReadFields");
      readEl.innerHTML = "";
      if (node.source_field_ids && node.source_field_ids.length > 0) {
        node.source_field_ids.slice(0, 15).forEach(f => {
          const tag = document.createElement("span");
          tag.className = "tag field-tag-read";
          tag.textContent = f;
          readEl.appendChild(tag);
        });
      } else {
        readEl.innerHTML = '<span style="font-size:0.8rem; color:var(--text-muted);">No variable reads</span>';
      }

      // Write Fields
      const writeEl = document.getElementById("inspWriteFields");
      writeEl.innerHTML = "";
      if (node.target_field_ids && node.target_field_ids.length > 0) {
        node.target_field_ids.slice(0, 15).forEach(f => {
          const tag = document.createElement("span");
          tag.className = "tag field-tag-write";
          tag.textContent = f;
          writeEl.appendChild(tag);
        });
      } else {
        writeEl.innerHTML = '<span style="font-size:0.8rem; color:var(--text-muted);">No variable writes</span>';
      }

      // Sync Selection in Cytoscape
      if (cy) {
        cy.nodes().unselect();
        const cyNode = cy.nodes().filter(n => (n.data("name") || n.data("label") || "").toUpperCase() === nodeName.toUpperCase());
        if (cyNode.length > 0) {
          cyNode.select();
        }
      }
    }
    // Note: renderCfgInspectorSection(node) is modularized in call_graph/js/linear_card.js.j2

    // Inspector Sidebar Toggle & Close Handling
    window.toggleInspector = function(forceOpen) {
      const inspector = document.getElementById("inspector");
      const splitter = document.getElementById("splitterInspector");
      const btnToggle = document.getElementById("btnToggleInspector");
      if (!inspector) return;

      const isHidden = inspector.style.display === "none";
      const shouldOpen = forceOpen !== undefined ? forceOpen : isHidden;

      if (shouldOpen) {
        inspector.style.display = "flex";
        if (splitter) splitter.style.display = "block";
        if (btnToggle) btnToggle.classList.add("active");
      } else {
        inspector.style.display = "none";
        if (splitter) splitter.style.display = "none";
        if (btnToggle) btnToggle.classList.remove("active");
      }

      if (cy) {
        setTimeout(() => cy.resize(), 30);
      }
    };

    const btnCloseInspector = document.getElementById("btnCloseInspector");
    if (btnCloseInspector) {
      btnCloseInspector.addEventListener("click", () => toggleInspector(false));
    }

    const btnToggleInspector = document.getElementById("btnToggleInspector");
    if (btnToggleInspector) {
      btnToggleInspector.addEventListener("click", () => toggleInspector());
    }

    // Procedure Details Popover Controller
    const btnRoutineInfo = document.getElementById("btnRoutineInfo");
    const routineInfoPopover = document.getElementById("routineInfoPopover");
    const btnCloseRoutineInfo = document.getElementById("btnCloseRoutineInfo");

    function toggleRoutineInfoPopover(forceState) {
      if (!routineInfoPopover) return;
      const shouldOpen = forceState !== undefined ? forceState : (routineInfoPopover.style.display === "none");
      routineInfoPopover.style.display = shouldOpen ? "block" : "none";
    }

    if (btnRoutineInfo) {
      btnRoutineInfo.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleRoutineInfoPopover();
      });
    }

    if (btnCloseRoutineInfo) {
      btnCloseRoutineInfo.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleRoutineInfoPopover(false);
      });
    }

    document.addEventListener("click", (e) => {
      if (routineInfoPopover && routineInfoPopover.style.display !== "none") {
        if (!routineInfoPopover.contains(e.target) && e.target !== btnRoutineInfo && !btnRoutineInfo.contains(e.target)) {
          toggleRoutineInfoPopover(false);
        }
      }
    });


/* --- linear_modal.js.j2 --- */

// -------------------------------------------------------------
    // Full Linear Procedure Card Modal
    // -------------------------------------------------------------
    function openLinearCardModal(node) {
      if (!node) node = selectedRoutineNode;
      if (!node) return;

      const modal = document.getElementById("linearModalBackdrop");
      if (!modal) return;

      document.getElementById("linearModalTitle").textContent = `Linear Procedure: ${node.name}`;
      document.getElementById("linearModalSubtitle").textContent = `Section: ${node.section || "DEFAULT"} | Lines: ${node.start_line > 0 ? 'L' + node.start_line + '-' + node.end_line : 'N/A'} | Complexity: CC 1 (Zero Branches)`;

      const stmts = node.cfg_linear_statements || [];
      document.getElementById("linearModalStmtCount").textContent = stmts.length;

      // Metrics row
      const metricsEl = document.getElementById("linearModalMetrics");
      metricsEl.innerHTML = "";

      const verbCounts = {};
      stmts.forEach(s => {
        const v = s.verb || "STATEMENT";
        verbCounts[v] = (verbCounts[v] || 0) + 1;
      });

      Object.entries(verbCounts).forEach(([verb, count]) => {
        const pill = document.createElement("span");
        pill.style.fontSize = "0.75rem";
        pill.style.fontWeight = "600";
        pill.style.padding = "4px 10px";
        pill.style.borderRadius = "6px";
        pill.style.background = "#F1F5F9";
        pill.style.color = "#334155";
        pill.style.border = "1px solid #E2E8F0";
        pill.textContent = `${verb}: ${count}`;
        metricsEl.appendChild(pill);
      });

      // Render Statement Table
      const tableEl = document.getElementById("linearModalTraceTable");
      tableEl.innerHTML = "";

      const table = document.createElement("table");
      table.style.width = "100%";
      table.style.borderCollapse = "collapse";
      table.style.fontSize = "0.85rem";
      table.style.fontFamily = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";

      const thead = document.createElement("thead");
      thead.innerHTML = `
        <tr style="background:#F8FAFC; border-bottom:1px solid #E2E8F0; text-align:left; color:#64748B; font-size:0.75rem; text-transform:uppercase;">
          <th style="padding:10px 14px; width:70px;">Line</th>
          <th style="padding:10px 14px; width:130px;">Operation</th>
          <th style="padding:10px 14px;">Statement Source</th>
        </tr>
      `;
      table.appendChild(thead);

      const tbody = document.createElement("tbody");
      stmts.forEach((s, idx) => {
        const tr = document.createElement("tr");
        tr.style.borderBottom = "1px solid #F1F5F9";
        if (idx % 2 === 1) tr.style.background = "#FAFAFA";

        const tdLine = document.createElement("td");
        tdLine.style.padding = "9px 14px";
        tdLine.style.color = "#94A3B8";
        tdLine.style.fontWeight = "600";
        tdLine.textContent = s.line ? `L${s.line}` : "L--";
        tr.appendChild(tdLine);

        const tdVerb = document.createElement("td");
        tdVerb.style.padding = "9px 14px";
        const verbSpan = document.createElement("span");
        verbSpan.style.fontWeight = "700";
        verbSpan.style.fontSize = "0.75rem";
        verbSpan.style.padding = "3px 8px";
        verbSpan.style.borderRadius = "4px";

        if (s.category === "data") {
          verbSpan.style.background = "#F0F4F8";
          verbSpan.style.color = "#245882";
        } else if (s.category === "call") {
          verbSpan.style.background = "#EBF3FC";
          verbSpan.style.color = "#0056B3";
        } else if (s.category === "io") {
          verbSpan.style.background = "#E8F5E9";
          verbSpan.style.color = "#198754";
        } else if (s.category === "terminal") {
          verbSpan.style.background = "#FDE8E8";
          verbSpan.style.color = "#C82333";
        } else {
          verbSpan.style.background = "#ECEFF2";
          verbSpan.style.color = "#4A5568";
        }
        verbSpan.textContent = s.verb || "STMT";
        tdVerb.appendChild(verbSpan);
        tr.appendChild(tdVerb);

        const tdText = document.createElement("td");
        tdText.style.padding = "9px 14px";
        tdText.style.color = "#0F172A";

        if ((s.category === "call" || s.category === "terminal") && s.target && graphData.nodes[s.target.toUpperCase()]) {
          tdText.innerHTML = `${escapeHtml(s.text.replace(s.target, ""))} <a href="#" style="color:#0078D4; font-weight:700; text-decoration:underline;">${escapeHtml(s.target)}</a>`;
          const a = tdText.querySelector("a");
          if (a) {
            a.onclick = (e) => {
              e.preventDefault();
              closeLinearCardModal();
              selectNode(s.target);
              focusNode(s.target);
            };
          }
        } else {
          tdText.textContent = s.text;
        }
        tr.appendChild(tdText);

        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      tableEl.appendChild(table);

      const copyBtn = document.getElementById("btnLinearCopy");
      const copyTextEl = document.getElementById("btnLinearCopyText");
      if (copyBtn) {
        copyBtn.onclick = () => {
          const lines = stmts.map(s => `${s.line ? 'L' + s.line + ': ' : ''}${s.text}`);
          navigator.clipboard.writeText(lines.join("\\n")).then(() => {
            const label = copyTextEl || copyBtn;
            const orig = label.textContent;
            label.textContent = "Copied!";
            setTimeout(() => { label.textContent = orig; }, 2000);
          });
        };
      }

      modal.style.display = "flex";
    }

    function closeLinearCardModal() {
      const modal = document.getElementById("linearModalBackdrop");
      if (modal) modal.style.display = "none";
    }

    const btnLinearCloseEl = document.getElementById("btnLinearClose");
    if (btnLinearCloseEl) {
      btnLinearCloseEl.addEventListener("click", closeLinearCardModal);
    }
    const linearModalBackdropEl = document.getElementById("linearModalBackdrop");
    if (linearModalBackdropEl) {
      linearModalBackdropEl.addEventListener("click", (e) => {
        if (e.target.id === "linearModalBackdrop") {
          closeLinearCardModal();
        }
      });
    }


/* --- level3_cfg.js.j2 --- */

// Level 3 Intra-Procedure Control Flow Graph (Cytoscape Modal)
    function openRoutineFlowModal(node) {
      if (!node) {
        alert("Please click or select a routine first.");
        return;
      }
      if (!node.is_cfg_eligible) {
        openLinearCardModal(node);
        return;
      }
      openLevel3Modal(node);
    }

    function openLevel3Modal(node) {
      if (!node) node = selectedRoutineNode;
      if (!node) {
        alert("Please click or select a routine first.");
        return;
      }
      if (!node.is_cfg_eligible) {
        openLinearCardModal(node);
        return;
      }

      CobolScopeLog.info(`Opening logic flowchart modal for routine: ${node.name}`);
      selectedRoutineNode = node;
      const modal = document.getElementById("cfgModalBackdrop");
      if (!modal) return;

      document.getElementById("cfgModalTitle").textContent = `Logic Flowchart: ${node.name}`;
      document.getElementById("cfgModalSubtitle").textContent = `Section: ${node.section || "DEFAULT"} | Complexity (CC): ${node.cyclomatic_complexity} | Statements: ${node.statement_count}`;
      modal.style.display = "flex";

      const container = document.getElementById("cy-cfg-container");
      if (cyLevel3) {
        cyLevel3.destroy();
        cyLevel3 = null;
      }

      const rawElements = node.cfg_elements || [];
      const nodeIds = new Set(rawElements.filter(e => !e.data.source).map(e => e.data.id));
      const elements = rawElements.filter(e => {
        if (!e.data.source) return true;
        return nodeIds.has(e.data.source) && nodeIds.has(e.data.target);
      });

      try {
        cyLevel3 = cytoscape({
          container: container,
          elements: elements,
          style: [
            {
              selector: "node",
              style: {
                "label": "data(label)",
                "text-wrap": "wrap",
                "text-valign": "center",
                "text-halign": "center",
                "font-family": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
                "font-size": 11,
                "font-weight": "600",
                "color": "#0F172A",
                "background-color": "#FFFFFF",
                "border-width": 2,
                "border-color": "#64748B",
                "shape": "round-rectangle",
                "padding": 12,
                "width": "label",
                "height": "label"
              }
            },
            {
              selector: "node.cfg-entry",
              style: {
                "background-color": "#F2F9F4",
                "border-color": "#107C41",
                "border-width": 2.5,
                "color": "#107C41",
                "shape": "round-rectangle"
              }
            },
            {
              selector: "node.cfg-exit",
              style: {
                "background-color": "#F8FAFC",
                "border-color": "#475569",
                "color": "#334155",
                "shape": "round-rectangle"
              }
            },
            {
              selector: "node.cfg-terminal",
              style: {
                "background-color": "#FEF2F2",
                "border-color": "#DC2626",
                "border-width": 2.5,
                "color": "#DC2626",
                "shape": "round-rectangle"
              }
            },
            {
              selector: "node.cfg-decision",
              style: {
                "shape": "diamond",
                "background-color": "#FFFBEB",
                "border-color": "#D97706",
                "border-width": 2.5,
                "color": "#92400E",
                "padding": 20
              }
            },
            {
              selector: "node.cfg-loop_header",
              style: {
                "shape": "hexagon",
                "background-color": "#FFF8E1",
                "border-color": "#B76E00",
                "border-width": 2.5,
                "color": "#7D4B00",
                "padding": 16
              }
            },
            {
              selector: "node.cfg-basic_block",
              style: {
                "shape": "round-rectangle",
                "background-color": "#F4F6F8",
                "border-color": "#0056B3",
                "border-width": 2,
                "color": "#1A202C",
                "font-family": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
                "font-size": 10.5,
                "text-halign": "center",
                "padding": 14,
                "line-height": 1.4
              }
            },
            {
              selector: "node.cfg-expandable",
              style: {
                "cursor": "pointer"
              }
            },
            {
              selector: "node.cfg-merge",
              style: {
                "shape": "round-rectangle",
                "background-color": "#F1F5F9",
                "border-color": "#94A3B8",
                "border-width": 1.5,
                "font-size": 9.5,
                "font-weight": "600",
                "color": "#475569",
                "padding": 6
              }
            },
            {
              selector: "node.cfg-unreachable",
              style: {
                "background-color": "#FEF2F2",
                "border-color": "#DC2626",
                "border-style": "dashed",
                "border-width": 2,
                "color": "#991B1B",
                "shape": "round-rectangle"
              }
            },
            {
              selector: "node.cfg-call_site",
              style: {
                "background-color": "#EBF3FC",
                "border-color": "#0056B3",
                "border-width": 2,
                "color": "#004494",
                "shape": "round-rectangle"
              }
            },
            {
              selector: "edge",
              style: {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "arrow-scale": 1.1,
                "line-color": "#A0AEC0",
                "target-arrow-color": "#A0AEC0",
                "width": 2,
                "label": "data(label)",
                "font-size": 9,
                "font-weight": "700",
                "text-background-color": "#FFFFFF",
                "text-background-opacity": 0.85,
                "text-background-padding": 2,
                "text-rotation": "autorotate"
              }
            },
            {
              selector: "edge.cfg-edge-true-branch",
              style: {
                "line-color": "#16A34A",
                "target-arrow-color": "#16A34A",
                "color": "#15803D",
                "width": 2.5
              }
            },
            {
              selector: "edge.cfg-edge-false-branch",
              style: {
                "line-color": "#DC2626",
                "target-arrow-color": "#DC2626",
                "color": "#B91C1C",
                "width": 2.5
              }
            },
            {
              selector: "edge.cfg-edge-when-branch",
              style: {
                "line-color": "#0284C7",
                "target-arrow-color": "#0284C7",
                "color": "#0369A1"
              }
            },
            {
              selector: "edge.cfg-edge-loop-body",
              style: {
                "line-color": "#B76E00",
                "target-arrow-color": "#B76E00",
                "color": "#7D4B00"
              }
            },
            {
              selector: "edge.cfg-edge-exception",
              style: {
                "line-color": "#DC2626",
                "target-arrow-color": "#DC2626",
                "color": "#B91C1C",
                "width": 2.5
              }
            },
            {
              selector: "edge.cfg-edge-fallthrough-default",
              style: {
                "line-color": "#64748B",
                "target-arrow-color": "#64748B",
                "color": "#475569",
                "line-style": "dashed"
              }
            }
          ],
          layout: {
            name: "dagre",
            rankDir: "TB",
            nodeSep: 35,
            rankSep: 40,
            padding: 30
          }
        });
        window.cyLevel3 = cyLevel3;

        // Click on expandable node to reveal all operations without zooming out the screen
        let isLayoutRunning = false;
        cyLevel3.on("tap", "node", (evt) => {
          const n = evt.target;
          if (n.data("is_expandable") && !isLayoutRunning) {
            isLayoutRunning = true;
            const isExp = !n.data("is_expanded");
            n.data("is_expanded", isExp);
            n.data("label", isExp ? n.data("full_label") : n.data("short_label"));

            const curZoom = cyLevel3.zoom();
            const curPan = cyLevel3.pan();
            const posBefore = { ...n.position() };

            cyLevel3.layout({
              name: "dagre",
              rankDir: "TB",
              nodeSep: 35,
              rankSep: 40,
              padding: 30,
              fit: false,           // Prevent screen from zooming out
              animate: true,
              animationDuration: 200,
              stop: () => {
                isLayoutRunning = false;
                // Anchor the expanded node in place
                const posAfter = n.position();
                const deltaX = (posBefore.x - posAfter.x) * curZoom;
                const deltaY = (posBefore.y - posAfter.y) * curZoom;
                cyLevel3.pan({
                  x: curPan.x + deltaX,
                  y: curPan.y + deltaY
                });
              }
            }).run();
          }
        });

        cyLevel3.fit(undefined, 30);
      } catch (err) {
        CobolScopeLog.error(`Level 3 Cytoscape layout error: ${err.message}`);
      }
    }

    function closeLevel3Modal() {
      const modal = document.getElementById("cfgModalBackdrop");
      if (modal) modal.style.display = "none";
      if (cyLevel3) {
        cyLevel3.destroy();
        cyLevel3 = null;
      }
    }

    document.getElementById("btnCfgClose").addEventListener("click", closeLevel3Modal);
    document.getElementById("btnCfgFit").addEventListener("click", () => { if (cyLevel3) cyLevel3.fit(undefined, 30); });
    document.getElementById("btnCfgReset").addEventListener("click", () => { if (cyLevel3) { cyLevel3.reset(); cyLevel3.fit(undefined, 30); } });

    const btnTopLevel3El = document.getElementById("btnTopLevel3");
    if (btnTopLevel3El) {
      btnTopLevel3El.addEventListener("click", () => {
        openRoutineFlowModal(selectedRoutineNode);
      });
    }

    document.getElementById("cfgModalBackdrop").addEventListener("click", (e) => {
      if (e.target.id === "cfgModalBackdrop") {
        closeLevel3Modal();
      }
    });


/* --- toolbar.js.j2 --- */

    const btnZoomIn = document.getElementById("btnZoomIn");
    if (btnZoomIn) {
      btnZoomIn.addEventListener("click", () => {
        if (cy) {
          cy.zoom(cy.zoom() * 1.2);
        }
      });
    }

    const btnZoomOut = document.getElementById("btnZoomOut");
    if (btnZoomOut) {
      btnZoomOut.addEventListener("click", () => {
        if (cy) {
          cy.zoom(cy.zoom() * 0.8);
        }
      });
    }

    const btnZoomReset = document.getElementById("btnZoomReset");
    if (btnZoomReset) {
      btnZoomReset.addEventListener("click", () => {
        clearHighlight();
        if (cy) {
          cy.reset();
          cy.fit(undefined, 40);
        }
      });
    }

    const btnFit = document.getElementById("btnFit");
    if (btnFit) {
      btnFit.addEventListener("click", () => {
        if (cy) {
          cy.fit(undefined, 40);
        }
      });
    }

    function clearHighlight() {
      if (cy) {
        cy.elements().removeClass("dimmed neighbor-highlight");
        cy.nodes().unselect();
      }
    }

    const btnJump = document.getElementById("btnJumpStart");
    if (btnJump) {
      btnJump.addEventListener("click", () => {
        const startKey = graphData.entry_point || Object.keys(graphData.nodes)[0];
        if (startKey) {
          selectNode(startKey);
          focusNode(startKey);
        }
      });
    }

    const searchInput = document.getElementById("nodeSearch");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const q = e.target.value.trim().toUpperCase();
        if (!q) {
          clearHighlight();
          return;
        }

        if (cy) {
          cy.elements().removeClass("dimmed neighbor-highlight");
          const matches = cy.nodes(".routine-node").filter(n => {
            const name = (n.data("name") || "").toUpperCase();
            const label = (n.data("label") || "").toUpperCase();
            const sec = (n.data("section") || "").toUpperCase();
            return name.includes(q) || label.includes(q) || sec.includes(q);
          });
          if (matches.length > 0) {
            const otherRoutines = cy.nodes(".routine-node").difference(matches);
            otherRoutines.addClass("dimmed");
            cy.edges().addClass("dimmed");
            matches.addClass("neighbor-highlight");
            const first = matches[0];
            selectNode(first.data("name") || first.data("label"));
            first.select();
          }
        }
      });
    }

    // Program Details Popover Controller
    const btnProgramInfo = document.getElementById("btnProgramInfo");
    const programInfoPopover = document.getElementById("programInfoPopover");
    const btnCloseProgramInfo = document.getElementById("btnCloseProgramInfo");

    function toggleProgramInfoPopover(forceState) {
      if (!programInfoPopover) return;
      const shouldOpen = forceState !== undefined ? forceState : (programInfoPopover.style.display === "none");
      programInfoPopover.style.display = shouldOpen ? "block" : "none";
    }

    if (btnProgramInfo) {
      btnProgramInfo.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleProgramInfoPopover();
      });
    }

    if (btnCloseProgramInfo) {
      btnCloseProgramInfo.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleProgramInfoPopover(false);
      });
    }

    document.addEventListener("click", (e) => {
      if (programInfoPopover && programInfoPopover.style.display !== "none") {
        if (!programInfoPopover.contains(e.target) && e.target !== btnProgramInfo && !btnProgramInfo.contains(e.target)) {
          toggleProgramInfoPopover(false);
        }
      }
    });

    // Header entry point click
    const hdrEntry = document.getElementById("hdrEntryPoint");
    if (hdrEntry && graphData.entry_point) {
      hdrEntry.addEventListener("click", () => {
        toggleProgramInfoPopover(false);
        selectNode(graphData.entry_point);
        focusNode(graphData.entry_point);
      });
    }

    // Keyboard Shortcuts (/ to search, Escape to close modals)
    window.addEventListener("keydown", (e) => {
      if (e.key === "/" && document.activeElement !== searchInput) {
        e.preventDefault();
        if (searchInput) searchInput.focus();
      } else if (e.key === "Escape") {
        toggleProgramInfoPopover(false);
        if (typeof toggleRoutineInfoPopover === "function") toggleRoutineInfoPopover(false);
        if (typeof closeLevel3Modal === "function") closeLevel3Modal();
        if (typeof closeLinearCardModal === "function") closeLinearCardModal();
      }
    });

    function escapeHtml(text) {
      if (!text) return "";
      return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    }

    function selectAndFocusRoutine(routineName, sectionName) {
      if (!routineName && !sectionName) return;
      const rUp = (routineName || "").trim().toUpperCase();
      const sUp = (sectionName || "").trim().toUpperCase();

      // 1. Direct match by node key
      if (rUp && graphData.nodes && graphData.nodes[rUp]) {
        selectNode(rUp);
        focusNode(rUp);
        return;
      }

      // 2. Direct match by section name in graphData.nodes
      if (sUp && graphData.nodes && graphData.nodes[sUp]) {
        selectNode(sUp);
        focusNode(sUp);
        return;
      }

      // 3. Match by node.name or node.section
      if (graphData.nodes) {
        for (const [k, n] of Object.entries(graphData.nodes)) {
          const nName = (n.name || "").trim().toUpperCase();
          const nSec = (n.section || "").trim().toUpperCase();
          if (rUp && (nName === rUp || nSec === rUp)) {
            selectNode(k);
            focusNode(k);
            return;
          }
          if (sUp && (nName === sUp || nSec === sUp)) {
            selectNode(k);
            focusNode(k);
            return;
          }
        }
      }

      // 4. Match in Cytoscape nodes
      if (cy) {
        const found = cy.nodes(".routine-node").filter(n => {
          const name = (n.data("name") || "").toUpperCase();
          const label = (n.data("label") || "").toUpperCase();
          const sec = (n.data("section") || "").toUpperCase();
          return (rUp && (name === rUp || label === rUp || sec === rUp)) ||
                 (sUp && (name === sUp || label === sUp || sec === sUp));
        });
        if (found.length > 0) {
          const first = found[0];
          const key = first.data("name") || first.data("label");
          selectNode(key);
          focusNode(key);
        }
      }
    }

    // Listen for postMessage from parent portal or other windows
    window.addEventListener("message", (e) => {
      if (e.data && e.data.type === "COBOLSCOPE_SELECT_ROUTINE") {
        selectAndFocusRoutine(e.data.routine, e.data.section);
      }
    });

    // Check URL hash/params for routine selection
    function checkUrlForRoutineSelection() {
      const hash = window.location.hash;
      const params = new URLSearchParams(window.location.search);
      let targetRoutine = params.get("routine");
      if (!targetRoutine && hash && hash.includes("routine=")) {
        const match = hash.match(/routine=([^&]+)/);
        if (match && match[1]) {
          targetRoutine = decodeURIComponent(match[1]);
        }
      }
      if (targetRoutine) {
        selectAndFocusRoutine(targetRoutine);
        return true;
      }
      return false;
    }

    window.addEventListener("hashchange", checkUrlForRoutineSelection);

    // Initialize View on DOM Ready
    function bootstrapCallGraph() {
      CobolScopeLog.info("Initializing Cytoscape Call Graph view...");
      if (typeof initCytoscape === "function") {
        initCytoscape();
      }
      const hasUrlRoutine = checkUrlForRoutineSelection();
      if (!hasUrlRoutine && typeof graphData !== "undefined" && graphData && graphData.nodes) {
        const startKey = graphData.entry_point || Object.keys(graphData.nodes)[0];
        if (startKey && typeof selectNode === "function") {
          selectNode(startKey);
        }
      }
    }

    if (document.readyState === "loading") {
      window.addEventListener("DOMContentLoaded", bootstrapCallGraph);
    } else {
      bootstrapCallGraph();
    }


/* --- code_viewer.js.j2 --- */

// Split-Screen Source Code Viewer & Workspace Resizers
(function() {
  const sourceCode = typeof sourceCodeRaw !== "undefined" ? sourceCodeRaw : "";
  const codeLines = sourceCode ? sourceCode.split(/\r?\n/) : [];

  const canvasEl = document.getElementById("canvas");
  const codeSplitPane = document.getElementById("codeSplitPane");
  const splitterCanvasCode = document.getElementById("splitterCanvasCode");
  const splitterInspector = document.getElementById("splitterInspector");
  const inspectorEl = document.getElementById("inspector");
  const workspaceMain = document.getElementById("workspaceMain");
  const btnToggleCodeSplit = document.getElementById("btnToggleCodeSplit");
  const btnCloseCodeSplit = document.getElementById("btnCloseCodeSplit");
  const codeJumpLineInput = document.getElementById("codeJumpLineInput");
  const codeCurrentRoutineBadge = document.getElementById("codeCurrentRoutineBadge");
  const codeLineCountInfo = document.getElementById("codeLineCountInfo");
  const codeEmptyState = document.getElementById("codeEmptyState");
  const cobolCodeTable = document.getElementById("cobolCodeTable");
  const cobolCodeTbody = document.getElementById("cobolCodeTbody");
  const btnViewRoutineCode = document.getElementById("btnViewRoutineCode");

  let isCodeSplitOpen = false;
  let currentStartLine = 0;
  let currentEndLine = 0;

  function escapeHtml(text) {
    if (!text) return "";
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function formatCodeLineHtml(lineText) {
    if (!lineText) return "";
    if (lineText.length >= 7 && (lineText[6] === "*" || lineText[6] === "/")) {
      return `<span class="code-comment">${escapeHtml(lineText)}</span>`;
    }
    const escaped = escapeHtml(lineText);
    return escaped.replace(/&(?:amp|lt|gt);|\b([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\b/g, (match, word) => {
      if (word) {
        return `<span class="code-word" data-word="${word.toUpperCase()}">${word}</span>`;
      }
      return match;
    });
  }

  let activeHighlightedWord = null;

  window.highlightWordInCode = function(wordToHighlight, forceState) {
    const norm = (wordToHighlight || "").toUpperCase().trim();
    if (!cobolCodeTbody) return;

    cobolCodeTbody.querySelectorAll(".code-word.var-highlight").forEach(el => {
      el.classList.remove("var-highlight");
    });

    if (!norm) {
      activeHighlightedWord = null;
      return;
    }

    if (forceState === undefined && norm === activeHighlightedWord) {
      activeHighlightedWord = null;
      return;
    }

    activeHighlightedWord = norm;
    const matches = cobolCodeTbody.querySelectorAll(`.code-word[data-word="${norm}"]`);
    matches.forEach(el => el.classList.add("var-highlight"));
  };

  // 1. Initial Render of Code Lines
  function renderSourceLines() {
    if (!codeLines || codeLines.length === 0) {
      if (codeEmptyState) codeEmptyState.style.display = "block";
      if (cobolCodeTable) cobolCodeTable.style.display = "none";
      if (codeLineCountInfo) codeLineCountInfo.textContent = "0 lines";
      return;
    }

    if (codeEmptyState) codeEmptyState.style.display = "none";
    if (cobolCodeTable) cobolCodeTable.style.display = "table";
    if (codeLineCountInfo) codeLineCountInfo.textContent = `${codeLines.length} lines`;

    const fragment = document.createDocumentFragment();
    for (let i = 0; i < codeLines.length; i++) {
      const lineNum = i + 1;
      const rawText = codeLines[i];

      const tr = document.createElement("tr");
      tr.id = `code-line-${lineNum}`;
      tr.className = "code-line-row";

      const tdNum = document.createElement("td");
      tdNum.className = "code-line-num";
      tdNum.textContent = lineNum;
      tdNum.title = `Line ${lineNum} (Click to select)`;
      tdNum.onclick = () => focusSingleLine(lineNum);

      const tdText = document.createElement("td");
      tdText.className = "code-line-text";

      const codeEl = document.createElement("code");
      codeEl.innerHTML = formatCodeLineHtml(rawText);
      tdText.appendChild(codeEl);

      tr.appendChild(tdNum);
      tr.appendChild(tdText);
      fragment.appendChild(tr);
    }

    cobolCodeTbody.innerHTML = "";
    cobolCodeTbody.appendChild(fragment);

    cobolCodeTbody.onclick = (e) => {
      const wordEl = e.target.closest(".code-word");
      if (wordEl && wordEl.dataset.word) {
        const w = wordEl.dataset.word;
        if (w.length >= 2 || /^[A-Z0-9]/.test(w)) {
          highlightWordInCode(w);
        }
      } else if (!e.target.closest(".code-line-num")) {
        highlightWordInCode(null);
      }
    };
  }

  // 2. Toggle Code Split Pane (Default: 65% Graph / 35% Code)
  window.toggleCodeSplit = function(forceState) {
    const targetState = forceState !== undefined ? forceState : !isCodeSplitOpen;
    isCodeSplitOpen = targetState;

    if (isCodeSplitOpen) {
      codeSplitPane.style.display = "flex";
      splitterCanvasCode.style.display = "block";
      if (btnToggleCodeSplit) btnToggleCodeSplit.classList.add("active");

      // Retrieve persisted ratio or use comfortable 42% Graph / 58% Code default
      let ratio = 42;
      const savedRatio = localStorage.getItem("cobolscope_code_split_ratio");
      if (savedRatio) {
        const parsed = parseFloat(savedRatio);
        if (!isNaN(parsed) && parsed >= 20 && parsed <= 80) {
          ratio = parsed;
        }
      }

      canvasEl.style.flex = `${ratio} 1 0px`;
      codeSplitPane.style.flex = `${100 - ratio} 1 0px`;

      if (cy) {
        setTimeout(() => cy.resize(), 30);
      }

      if (selectedRoutineNode) {
        highlightRoutineInCode(selectedRoutineNode.start_line, selectedRoutineNode.end_line, selectedRoutineNode.name, selectedRoutineNode.source_file);
      }
    } else {
      codeSplitPane.style.display = "none";
      splitterCanvasCode.style.display = "none";
      canvasEl.style.flex = "1 1 0px";
      if (btnToggleCodeSplit) btnToggleCodeSplit.classList.remove("active");

      if (cy) {
        setTimeout(() => cy.resize(), 30);
      }
    }

    localStorage.setItem("cobolscope_code_split_open", isCodeSplitOpen ? "true" : "false");
  };

  // 3. Highlight Procedure / Routine Lines
  window.highlightRoutineInCode = function(startLine, endLine, routineName, sourceFile) {
    if (!codeLines || codeLines.length === 0) return;

    // Clear previous line highlights
    const prevHighlighted = cobolCodeTbody.querySelectorAll(".line-highlighted, .line-highlight-start");
    prevHighlighted.forEach(el => el.classList.remove("line-highlighted", "line-highlight-start"));

    currentStartLine = startLine || 0;
    currentEndLine = endLine || 0;

    const mainFile = (typeof graphData !== "undefined" && graphData.source_file) ? graphData.source_file : "";
    const isCopybook = Boolean(sourceFile && mainFile && !mainFile.endsWith(sourceFile) && !sourceFile.endsWith(mainFile));

    if (routineName) {
      const lineSpanText = currentStartLine > 0 ? `(L${currentStartLine}-L${currentEndLine})` : "";
      if (isCopybook) {
        codeCurrentRoutineBadge.textContent = `[COPYBOOK: ${sourceFile}] ${routineName} ${lineSpanText}`.trim();
      } else {
        codeCurrentRoutineBadge.textContent = `[ROUTINE] ${routineName} ${lineSpanText}`.trim();
      }
    } else {
      codeCurrentRoutineBadge.textContent = "No routine selected";
    }

    if (!isCopybook && currentStartLine > 0 && currentEndLine >= currentStartLine) {
      for (let l = currentStartLine; l <= currentEndLine; l++) {
        const row = document.getElementById(`code-line-${l}`);
        if (row) {
          row.classList.add("line-highlighted");
          if (l === currentStartLine) {
            row.classList.add("line-highlight-start");
          }
        }
      }

      // Scroll smoothly to start line
      const firstRow = document.getElementById(`code-line-${currentStartLine}`);
      if (firstRow) {
        firstRow.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  };

  function focusSingleLine(lineNum) {
    const prevHighlighted = cobolCodeTbody.querySelectorAll(".line-highlighted, .line-highlight-start");
    prevHighlighted.forEach(el => el.classList.remove("line-highlighted", "line-highlight-start"));

    const row = document.getElementById(`code-line-${lineNum}`);
    if (row) {
      row.classList.add("line-highlighted", "line-highlight-start");
      row.scrollIntoView({ behavior: "smooth", block: "center" });
      codeCurrentRoutineBadge.textContent = `[LINE] ${lineNum}`;
    }
  }

  // 4. Jump to Line or Search in Code
  function handleCodeJumpOrSearch() {
    const val = (codeJumpLineInput.value || "").trim();
    if (!val) return;

    if (/^\d+$/.test(val)) {
      const lineNum = parseInt(val, 10);
      if (lineNum >= 1 && lineNum <= codeLines.length) {
        focusSingleLine(lineNum);
      }
    } else {
      // Text search in source lines
      const q = val.toUpperCase();
      let foundLine = 0;
      for (let i = 0; i < codeLines.length; i++) {
        if (codeLines[i].toUpperCase().includes(q)) {
          foundLine = i + 1;
          break;
        }
      }
      if (foundLine > 0) {
        focusSingleLine(foundLine);
      }
    }
  }

  if (codeJumpLineInput) {
    codeJumpLineInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleCodeJumpOrSearch();
      }
    });
  }

  if (btnCloseCodeSplit) {
    btnCloseCodeSplit.addEventListener("click", () => toggleCodeSplit(false));
  }

  if (btnToggleCodeSplit) {
    btnToggleCodeSplit.addEventListener("click", () => toggleCodeSplit());
  }

  if (btnViewRoutineCode) {
    btnViewRoutineCode.addEventListener("click", () => {
      if (!isCodeSplitOpen) {
        toggleCodeSplit(true);
      }
      if (selectedRoutineNode) {
        highlightRoutineInCode(selectedRoutineNode.start_line, selectedRoutineNode.end_line, selectedRoutineNode.name, selectedRoutineNode.source_file);
      }
    });
  }

  // 5. Draggable Divider: Graph Canvas <-> Code Split Pane
  function setupCanvasCodeSplitter() {
    if (!splitterCanvasCode || !canvasEl || !codeSplitPane || !workspaceMain) return;

    let isDragging = false;

    splitterCanvasCode.addEventListener("pointerdown", (e) => {
      isDragging = true;
      splitterCanvasCode.setPointerCapture(e.pointerId);
      document.body.classList.add("is-resizing");
      splitterCanvasCode.classList.add("active");
      e.preventDefault();
    });

    splitterCanvasCode.addEventListener("pointermove", (e) => {
      if (!isDragging) return;
      const rect = workspaceMain.getBoundingClientRect();
      const currentX = e.clientX - rect.left;
      let ratio = (currentX / rect.width) * 100;

      // Bound ratio strictly between 20% and 80%
      ratio = Math.max(20, Math.min(80, ratio));

      canvasEl.style.flex = `${ratio} 1 0px`;
      codeSplitPane.style.flex = `${100 - ratio} 1 0px`;

      localStorage.setItem("cobolscope_code_split_ratio", ratio.toFixed(1));

      if (cy) {
        cy.resize();
      }
    });

    const stopDrag = (e) => {
      if (isDragging) {
        isDragging = false;
        document.body.classList.remove("is-resizing");
        splitterCanvasCode.classList.remove("active");
        try { splitterCanvasCode.releasePointerCapture(e.pointerId); } catch (_) {}
        if (cy) {
          cy.resize();
        }
      }
    };

    splitterCanvasCode.addEventListener("pointerup", stopDrag);
    splitterCanvasCode.addEventListener("pointercancel", stopDrag);
  }

  // 6. Draggable Divider: Workspace Main <-> Inspector Sidebar
  function setupInspectorSplitter() {
    if (!splitterInspector || !inspectorEl) return;

    let isDragging = false;

    // Restore saved inspector width
    const savedWidth = localStorage.getItem("cobolscope_inspector_width");
    if (savedWidth) {
      const parsed = parseInt(savedWidth, 10);
      if (!isNaN(parsed) && parsed >= 260 && parsed <= 600) {
        inspectorEl.style.width = `${parsed}px`;
      }
    }

    splitterInspector.addEventListener("pointerdown", (e) => {
      isDragging = true;
      splitterInspector.setPointerCapture(e.pointerId);
      document.body.classList.add("is-resizing");
      splitterInspector.classList.add("active");
      e.preventDefault();
    });

    splitterInspector.addEventListener("pointermove", (e) => {
      if (!isDragging) return;
      const workspaceRect = document.querySelector(".workspace").getBoundingClientRect();
      const newWidth = workspaceRect.right - e.clientX;

      // Bounds: 260px - 600px
      const clampedWidth = Math.max(260, Math.min(600, newWidth));
      inspectorEl.style.width = `${clampedWidth}px`;

      localStorage.setItem("cobolscope_inspector_width", clampedWidth.toString());

      if (cy) {
        cy.resize();
      }
    });

    const stopDrag = (e) => {
      if (isDragging) {
        isDragging = false;
        document.body.classList.remove("is-resizing");
        splitterInspector.classList.remove("active");
        try { splitterInspector.releasePointerCapture(e.pointerId); } catch (_) {}
        if (cy) {
          cy.resize();
        }
      }
    };

    splitterInspector.addEventListener("pointerup", stopDrag);
    splitterInspector.addEventListener("pointercancel", stopDrag);
  }

  // 7. Global Keyboard Shortcut [Alt+C] to toggle Code View
  document.addEventListener("keydown", (e) => {
    if (e.altKey && (e.key === "c" || e.key === "C")) {
      e.preventDefault();
      toggleCodeSplit();
    }
  });

  // Initialize
  renderSourceLines();
  setupCanvasCodeSplitter();
  setupInspectorSplitter();

  // Restore split view state if user previously had it open and source exists
  const wasOpen = localStorage.getItem("cobolscope_code_split_open") === "true";
  if (wasOpen && sourceCode) {
    toggleCodeSplit(true);
  }
})();



  // -------------------------------------------------------------
  // CobolScope Global Controller & Auto-Init
  // -------------------------------------------------------------
  const CobolScope = {
    version: "0.1.0",
    isInitialized: false,

    init: function() {
      if (this.isInitialized) return;
      populateDataIsland();
      if (typeof bootstrapCallGraph === 'function') {
        bootstrapCallGraph();
      } else if (typeof initCytoscape === 'function') {
        initCytoscape();
      }
      this.isInitialized = true;
    }
  };

  window.CobolScope = CobolScope;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => CobolScope.init());
  } else {
    CobolScope.init();
  }

})(window, document);
