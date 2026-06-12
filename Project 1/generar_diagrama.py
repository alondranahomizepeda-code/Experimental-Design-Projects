import graphviz
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

# Inicializar el lienzo del diagrama (Top to Bottom)
dot = graphviz.Digraph('Flujo_Experimento', format='png')
dot.attr(rankdir='TB', compound='true')

# Configurar el estilo global (Blanco y Negro, fuente Arial)
dot.attr('node', fontname='Arial', shape='rectangle', color='black', fillcolor='white', style='filled', penwidth='1.5')
dot.attr('edge', fontname='Arial', color='black', penwidth='1.0')

# --- BLOQUE IZQUIERDO: PROGRAMA PRINCIPAL ---
with dot.subgraph(name='cluster_main') as main:
    main.attr(label='Main Program Flow', style='dashed', color='black', fontname='Arial', fontsize='14')
    
    main.node('M1', 'Start', shape='oval')
    main.node('M2', 'Configure Ports\n& Variables')
    main.node('M3', 'Phase Cold?', shape='diamond')
    main.node('M4', 'Call registrar_fase()')
    main.node('M5', 'Phase Warm?', shape='diamond')
    main.node('M6', 'Call registrar_fase()')
    main.node('M7', 'Phase Hot?', shape='diamond')
    main.node('M8', 'Call registrar_fase()')
    main.node('M9', 'Export CSV Data')
    main.node('M10', 'End', shape='oval')

    # Flechas
    main.edges([('M1', 'M2'), ('M2', 'M3')])
    main.edge('M3', 'M4', label=' Yes')
    main.edge('M3', 'M5', label=' No')
    main.edge('M4', 'M5')
    main.edge('M5', 'M6', label=' Yes')
    main.edge('M5', 'M7', label=' No')
    main.edge('M6', 'M7')
    main.edge('M7', 'M8', label=' Yes')
    main.edge('M7', 'M9', label=' No')
    main.edge('M8', 'M9')
    main.edge('M9', 'M10')

# --- BLOQUE DERECHO: SUBRUTINA ---
with dot.subgraph(name='cluster_sub') as sub:
    sub.attr(label='Subroutine: registrar_fase', style='dashed', color='black', fontname='Arial', fontsize='14')
    
    sub.node('S1', 'Start Routine', shape='oval')
    sub.node('S2', 'Open Serial &\nWait 2.5s')
    sub.node('S3', 'Clear Buffer')
    sub.node('S4', 'Samples < 10?', shape='diamond')
    sub.node('S5', 'Read, Decode\n& Append')
    sub.node('S6', 'Close Serial Port')
    sub.node('S7', 'Calculate Mean\n& Variance')
    sub.node('S8', 'Return Data', shape='oval')

    # Flechas
    sub.edges([('S1', 'S2'), ('S2', 'S3'), ('S3', 'S4')])
    sub.edge('S4', 'S5', label=' Yes')
    sub.edge('S5', 'S4') 
    sub.edge('S4', 'S6', label=' No')
    sub.edges([('S6', 'S7'), ('S7', 'S8')])

# --- GENERAR IMAGEN ---
try:
    # Se guardará como diagrama_flujo.png en tu carpeta actual
    archivo_salida = dot.render('diagrama_flujo', view=False)
    print(f"\n[+] ¡Éxito! El diagrama se ha generado: {archivo_salida}")
except graphviz.backend.execute.ExecutableNotFound:
    print("\n[-] Error: Reinicia VS Code para que reconozca Graphviz.")