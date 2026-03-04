"""
First Phosphate Corp (CSE: PHOS) — Financial Analysis
Pure full-screen Excel experience via Luckysheet.
"""

import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(
    page_title="PHOS Financial Analysis",
    page_icon="⛏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, header, footer, .stDeployButton,
    div[data-testid="stToolbar"], div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"], section[data-testid="stSidebar"],
    .stApp > header { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    .stApp { overflow: hidden !important; }
    .element-container { margin: 0 !important; padding: 0 !important; }
    iframe { border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)


def get_xlsx_base64():
    with open("data.xlsx", "rb") as f:
        return base64.b64encode(f.read()).decode()


xlsx_b64 = get_xlsx_base64()

html = f"""<!DOCTYPE html><html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/luckysheet@2.1.13/dist/plugins/css/pluginsCss.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/luckysheet@2.1.13/dist/plugins/plugins.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/luckysheet@2.1.13/dist/css/luckysheet.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/luckysheet@2.1.13/dist/assets/iconfont/iconfont.css"/>
<script src="https://cdn.jsdelivr.net/npm/luckysheet@2.1.13/dist/plugins/js/plugin.js"></script>
<script src="https://cdn.jsdelivr.net/npm/luckysheet@2.1.13/dist/luckysheet.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/luckyexcel@1.0.1/dist/luckyexcel.umd.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{height:100%;width:100%;overflow:hidden;background:#0e1117;touch-action:manipulation}}
#luckysheet{{position:absolute;top:0;left:0;right:0;bottom:0}}
.luckysheet-wa-editor,.luckysheet-grid-window{{background:#0e1117!important}}
.luckysheet-cell-input{{background:#1a1a2e!important;color:#fff!important}}
.luckysheet-sheets-item{{background:#1a1a2e!important;color:#ccc!important;border-color:#333!important}}
.luckysheet-sheets-item-active{{background:#0f3460!important;color:#fff!important}}
.luckysheet-sheet-area,.luckysheet-sheet-container{{background:#0e1117!important;border-color:#333!important}}
.luckysheet-toolbar{{background:#0e1117!important;border-color:#333!important}}
.luckysheet-toolbar-button{{color:#ccc!important}}
.luckysheet-cols-h-cells,.luckysheet-rows-h{{background:#16213e!important;color:#888!important}}
.luckysheet-scrollbar-x,.luckysheet-scrollbar-y{{background:#1a1a2e!important}}
.luckysheet-stat-area{{background:#0e1117!important;color:#888!important;border-color:#333!important}}
.luckysheet-input-box{{background:#1a1a2e!important;color:#fff!important;border-color:#333!important}}
.luckysheet-wa-functionbox{{background:#0e1117!important;border-color:#333!important}}
.luckysheet-wa-functionbox-cancel,.luckysheet-wa-functionbox-confirm{{background:#1a1a2e!important;color:#ccc!important}}
.luckysheet-name-box{{background:#1a1a2e!important;color:#fff!important;border-color:#333!important}}
.luckysheet-toolbar-menu-line{{border-color:#333!important}}
.luckysheet-cell-selected{{border-color:#e94560!important}}
.luckysheet-column-selected,.luckysheet-row-selected{{background:rgba(233,69,96,0.1)!important}}
.luckysheet-cols-menu,.luckysheet-rightclick-menu{{background:#1a1a2e!important;border-color:#333!important;color:#ccc!important}}
.luckysheet-cols-menuitem:hover,.luckysheet-rightclick-menu-item:hover{{background:#0f3460!important}}
.luckysheet-modal-dialog{{background:#1a1a2e!important;border-color:#333!important;color:#ccc!important}}
.luckysheet-modal-dialog-title-text{{color:#fff!important}}
@media(max-width:768px){{
    .luckysheet-toolbar{{overflow-x:auto!important;white-space:nowrap!important;-webkit-overflow-scrolling:touch}}
    .luckysheet-toolbar-button{{padding:2px 3px!important;min-width:24px!important}}
    .luckysheet-name-box{{width:50px!important;font-size:11px!important}}
    .luckysheet-wa-functionbox{{font-size:12px!important}}
    .luckysheet-sheets-item{{padding:4px 8px!important;font-size:11px!important}}
}}
</style>
</head><body>
<div id="luckysheet"></div>
<script>
var b64="{xlsx_b64}";
var bin=atob(b64);var u8=new Uint8Array(bin.length);
for(var i=0;i<bin.length;i++)u8[i]=bin.charCodeAt(i);
var blob=new Blob([u8],{{type:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}});
LuckyExcel.transformExcelToLucky(blob,function(ej){{
    if(!ej||!ej.sheets||!ej.sheets.length){{
        document.getElementById('luckysheet').innerHTML='<p style="color:#e94560;padding:20px;font-family:sans-serif">Failed to load. Refresh the page.</p>';
        return;
    }}
    ej.sheets[0].status=1;
    for(var i=1;i<ej.sheets.length;i++)ej.sheets[i].status=0;
    window.luckysheet.create({{
        container:'luckysheet',
        data:ej.sheets,
        title:'',
        showtoolbar:true,
        showinfobar:false,
        showsheetbar:true,
        showstatisticBar:true,
        sheetBottomConfig:true,
        allowEdit:true,
        enableAddRow:true,
        enableAddBackTop:false,
        showConfigWindowResize:false,
        forceCalculation:true,
        defaultFontSize:11,
        gridKey:'phos',
        loadUrl:'',
        plugins:['chart'],
    }});
    window.addEventListener('resize',function(){{try{{window.luckysheet.resize()}}catch(e){{}}}});
}});
</script></body></html>"""

components.html(html, height=900, scrolling=False)
