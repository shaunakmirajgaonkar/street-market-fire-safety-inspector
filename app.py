from pathlib import Path
import base64
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from firewatch_engine import REQUIRED_METRICS, REQUIRED_HISTORY, score_markets, validate_schema, summary

st.set_page_config(page_title='FireWatch | Street-Market Fire Safety Inspector', page_icon='🔥', layout='wide', initial_sidebar_state='expanded')

ROOT = Path(__file__).parent

def svg_data(path):
    p = ROOT / path
    return base64.b64encode(p.read_bytes()).decode('utf-8') if p.exists() else ''

st.markdown('''
<style>
:root{--navy:#12315a;--blue:#2677e8;--teal:#1fa38b;--amber:#f4a340;--red:#ef5b5b;--violet:#7b61ff;--ink:#19304f;--muted:#607998;--panel:#ffffff;--bg:#f4f8fc}
.stApp{background:linear-gradient(180deg,#f8fbff 0%,#f1f7fb 100%);color:var(--ink)}
.block-container{padding-top:1.15rem;padding-bottom:2rem;max-width:1500px}
.hero{background:linear-gradient(120deg,#eaf5ff 0%,#effcf7 55%,#fff8ea 100%);border:1px solid #d9e7f2;border-radius:28px;padding:24px 28px;box-shadow:0 14px 35px rgba(45,77,118,.09);margin-bottom:22px}
.hero-grid{display:grid;grid-template-columns:110px minmax(0,1fr) 260px;gap:24px;align-items:center}
.hero-logo{width:92px;height:92px;border-radius:24px;background:#fff;display:flex;align-items:center;justify-content:center;border:1px solid #d9e7f2;box-shadow:0 8px 20px rgba(29,69,110,.08)}
.hero-logo img{width:62px;height:62px}
.hero h1{font-size:42px;line-height:1.08;margin:0;color:#163e71;letter-spacing:-.8px}
.hero p{margin:.45rem 0 0;color:#607998;font-size:17px}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.badge{background:#fff;border:1px solid #d7e4ef;border-radius:999px;padding:7px 11px;color:#24466f;font-weight:600;font-size:13px}
.hero-callout{background:#ffffffc9;border:1px solid #d6e8e0;border-radius:20px;padding:18px;text-align:center}.hero-callout strong{display:block;font-size:19px;color:#19745b}.hero-callout span{display:block;color:#6b809b;margin-top:6px;font-size:13px}
.section-title{font-size:25px;font-weight:800;color:#193f70;margin:.2rem 0 .25rem}.section-sub{color:#6d829d;margin-bottom:16px}
.kpi{background:#fff;border:1px solid #dbe7f0;border-radius:20px;padding:18px 18px 15px;box-shadow:0 10px 24px rgba(50,78,110,.06);min-height:118px}.kpi-label{color:#6f829a;font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.7px}.kpi-value{font-size:34px;line-height:1.05;font-weight:900;color:#173e72;margin-top:10px}.kpi-note{margin-top:8px;color:#5c8b7a;font-size:13px}
.panel{background:#fff;border:1px solid #dbe7f0;border-radius:20px;padding:18px;box-shadow:0 10px 24px rgba(50,78,110,.05);height:100%}
.small-note{font-size:12px;color:#7690aa}
[data-testid='stSidebar']{background:linear-gradient(180deg,#edf6fd 0%,#f6fbff 100%);border-right:1px solid #dbe7f0}
[data-testid='stSidebar'] .block-container{padding-top:1.3rem}
.sidebar-brand{background:#fff;border:1px solid #d7e5ef;border-radius:20px;padding:14px;margin-bottom:16px;text-align:center}.sidebar-brand img{width:54px;height:54px}.sidebar-brand h3{margin:.2rem 0 0;color:#143d70}.sidebar-brand p{margin:.25rem 0 0;color:#6f8299;font-size:12px}
.stButton>button{border-radius:12px;border:1px solid #d7e5ef;background:#fff;color:#234b78;font-weight:700;padding:.45rem .8rem}.stButton>button:hover{border-color:#9dc0e8;color:#173e72}
[data-testid='stMetricValue']{color:#173e72}
@media (max-width:1100px){.hero-grid{grid-template-columns:82px minmax(0,1fr)}.hero-callout{grid-column:1/-1}.hero h1{font-size:34px}}
</style>
''', unsafe_allow_html=True)

logo = svg_data('assets/firewatch_logo.svg')
st.sidebar.markdown(f'''<div class="sidebar-brand"><img src="data:image/svg+xml;base64,{logo}"><h3>FireWatch</h3><p>Street-Market Fire Safety Inspector</p></div>''', unsafe_allow_html=True)
page = st.sidebar.radio('Navigation', ['Command Center','Market Risk','Safety Controls','Inspection History','Scenario Lab','Data Upload','Reports'])
st.sidebar.markdown('---')
st.sidebar.info('LOCAL PROCESSING\n\nCSV • Pandas • NumPy • Plotly\n\nNo external APIs required.')

metrics_path = ROOT/'data/sample_market_metrics.csv'; history_path = ROOT/'data/sample_inspection_history.csv'
metrics = pd.read_csv(metrics_path); history = pd.read_csv(history_path)

if 'metrics_df' not in st.session_state: st.session_state.metrics_df = metrics.copy()
if 'history_df' not in st.session_state: st.session_state.history_df = history.copy()
metrics = st.session_state.metrics_df; history = st.session_state.history_df
scored = score_markets(metrics)
sumv = summary(scored)

st.markdown(f'''<div class="hero"><div class="hero-grid"><div class="hero-logo"><img src="data:image/svg+xml;base64,{logo}"></div><div><h1>Street-Market Fire Safety Inspector</h1><p>Fire-risk screening for stalls, wiring, exits, fuel storage, hydrant access, and inspection history — processed locally.</p><div class="badges"><span class="badge">100% Local</span><span class="badge">Explainable Scoring</span><span class="badge">Fire-Safety Focus</span><span class="badge">Operational Planning</span></div></div><div class="hero-callout"><strong>Prevent Before the Spark</strong><span>Inspect • Reduce • Protect</span></div></div></div>''', unsafe_allow_html=True)

if page == 'Command Center':
    st.markdown('<div class="section-title">Command Center</div><div class="section-sub">Operational overview of fire exposure, access constraints, inspection status, and priority markets.</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    vals=[('MARKET AREAS',f"{sumv['markets']}",'Monitored market locations'),('AVG RISK',f"{sumv['avg_score']:.1f}",'Explainable 0–100 score'),('HIGH / CRITICAL',f"{sumv['high_critical']}",'Priority review group'),('CRITICAL',f"{sumv['critical']}",'Immediate review signal'),('OVERDUE INSPECTIONS',f"{sumv['inspection_overdue']}",'>30 days since inspection')]
    for c,(l,v,n) in zip(cols,vals): c.markdown(f'<div class="kpi"><div class="kpi-label">{l}</div><div class="kpi-value">{v}</div><div class="kpi-note">{n}</div></div>',unsafe_allow_html=True)
    st.write('')
    a,b,c=st.columns([1.15,1,1])
    with a:
        st.markdown('<div class="panel"><b>Risk Level Distribution</b>',unsafe_allow_html=True)
        counts=scored['risk_level'].value_counts().reindex(['Low','Moderate','High','Critical']).fillna(0).astype(int)
        fig=px.pie(values=counts.values,names=counts.index,hole=.58)
        fig.update_layout(height=330,margin=dict(l=10,r=10,t=35,b=10),legend_title_text='')
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False}); st.markdown('</div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel"><b>Primary Risk Drivers</b>',unsafe_allow_html=True)
        drv=scored['primary_driver'].value_counts().head(8).reset_index(); drv.columns=['driver','markets']
        fig=px.bar(drv,x='markets',y='driver',orientation='h')
        fig.update_layout(height=330,margin=dict(l=0,r=10,t=35,b=10),yaxis_title='',xaxis_title='Market areas')
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False}); st.markdown('</div>',unsafe_allow_html=True)
    with c:
        st.markdown('<div class="panel"><b>Risk vs Stall Density</b>',unsafe_allow_html=True)
        fig=px.scatter(scored,x='stall_density_per_100m',y='fire_risk_score',size='stall_count',hover_name='market_name',color='risk_level',size_max=28)
        fig.update_layout(height=330,margin=dict(l=0,r=10,t=35,b=10),xaxis_title='Stalls / 100m',yaxis_title='Risk score')
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False}); st.markdown('</div>',unsafe_allow_html=True)
    st.write('')
    d,e=st.columns([1.2,1])
    with d:
        st.markdown('<div class="panel"><b>Priority Markets</b>',unsafe_allow_html=True)
        top=scored.sort_values('fire_risk_score',ascending=False)[['market_name','zone','fire_risk_score','risk_level','primary_driver']].head(8)
        st.dataframe(top,width='stretch',hide_index=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with e:
        st.markdown('<div class="panel"><b>Recommended Operational Actions</b>',unsafe_allow_html=True)
        high=sumv['high_critical']; overdue=sumv['inspection_overdue']
        items=[f"Re-inspect {high} high/critical market areas first.",f"Review {overdue} locations with inspections older than 30 days.","Check fuel-storage separation and electrical wiring before peak trading periods.","Confirm hydrant access and unobstructed exits at high-density zones.","Use the scenario lab to test the effect of improved controls."]
        for i,item in enumerate(items,1): st.markdown(f"**{i}.** {item}")
        st.markdown('<div class="small-note">These are screening-based operational prompts, not a substitute for fire-authority inspection.</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

elif page == 'Market Risk':
    st.markdown('<div class="section-title">Market Risk Explorer</div><div class="section-sub">Filter and inspect fire-risk signals across market areas.</div>', unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    zones=sorted(scored['zone'].unique()); levels=['All','Low','Moderate','High','Critical']
    z=c1.selectbox('Zone',['All']+zones); lvl=c2.selectbox('Risk level',levels); sort_col=c3.selectbox('Rank by',['fire_risk_score','stall_density_per_100m','electrical_wiring_risk','fuel_storage_risk','inspection_overdue_days'])
    view=scored.copy()
    if z!='All': view=view[view['zone']==z]
    if lvl!='All': view=view[view['risk_level']==lvl]
    view=view.sort_values(sort_col,ascending=False)
    st.dataframe(view[['market_id','market_name','zone','stall_count','stall_density_per_100m','electrical_wiring_risk','exit_access_score','fuel_storage_risk','hydrant_access_score','inspection_overdue_days','recent_incident_count_90d','fire_extinguisher_coverage_pct','fire_risk_score','risk_level','primary_driver']],width='stretch',hide_index=True)
    st.download_button('Download filtered market risk CSV',view.to_csv(index=False).encode(),'firewatch_filtered_market_risk.csv','text/csv')

elif page == 'Safety Controls':
    st.markdown('<div class="section-title">Safety Controls</div><div class="section-sub">Inspect the operational controls that most influence the screening score.</div>', unsafe_allow_html=True)
    metrics2=scored.copy();
    for col,label in [('electrical_wiring_risk','Electrical wiring risk'),('fuel_storage_risk','Fuel storage risk'),('exit_access_score','Exit access score'),('hydrant_access_score','Hydrant access score'),('fire_extinguisher_coverage_pct','Extinguisher coverage')]:
        left,right=st.columns([1,2])
        with left: st.metric(label, f"{metrics2[col].mean():.1f}")
        with right:
            fig=px.histogram(metrics2,x=col,color='risk_level',nbins=10)
            fig.update_layout(height=170,margin=dict(l=0,r=0,t=10,b=10),xaxis_title='',yaxis_title='Markets')
            st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

elif page == 'Inspection History':
    st.markdown('<div class="section-title">Inspection History</div><div class="section-sub">Review inspection scores and historical control signals by market.</div>', unsafe_allow_html=True)
    selected=st.selectbox('Market',scored['market_name'].tolist()); mid=scored.loc[scored['market_name']==selected,'market_id'].iloc[0]
    h=history[history['market_id']==mid].copy(); h['inspection_date']=pd.to_datetime(h['inspection_date'])
    if h.empty: st.info('No history for this market.')
    else:
        f=px.line(h.sort_values('inspection_date'),x='inspection_date',y='inspection_score',markers=True)
        f.update_layout(height=320,margin=dict(l=0,r=0,t=20,b=10),yaxis_title='Inspection score',xaxis_title='')
        st.plotly_chart(f,width='stretch',config={'displayModeBar':False})
        st.dataframe(h.sort_values('inspection_date',ascending=False),width='stretch',hide_index=True)

elif page == 'Scenario Lab':
    st.markdown('<div class="section-title">Scenario Lab</div><div class="section-sub">Test how stronger controls could change the screening score. Scenario values remain local and are not saved.</div>', unsafe_allow_html=True)
    name=st.selectbox('Select market',scored['market_name'].tolist()); base=metrics.loc[metrics['market_name']==name].iloc[0].copy()
    a,b,c=st.columns(3)
    wiring=a.slider('Electrical wiring risk',0.0,100.0,float(base.electrical_wiring_risk),1.0)
    fuel=b.slider('Fuel storage risk',0.0,100.0,float(base.fuel_storage_risk),1.0)
    exits=c.slider('Exit access score',0.0,100.0,float(base.exit_access_score),1.0)
    d,e,f=st.columns(3)
    hydr=e.slider('Hydrant access score',0.0,100.0,float(base.hydrant_access_score),1.0)
    exting=d.slider('Extinguisher coverage %',0.0,100.0,float(base.fire_extinguisher_coverage_pct),1.0)
    crowd=f.slider('Crowding index',0.0,100.0,float(base.crowding_index),1.0)
    row=base.copy(); row['electrical_wiring_risk']=wiring; row['fuel_storage_risk']=fuel; row['exit_access_score']=exits; row['hydrant_access_score']=hydr; row['fire_extinguisher_coverage_pct']=exting; row['crowding_index']=crowd
    scen=score_markets(pd.DataFrame([row])).iloc[0]
    orig=float(scored.loc[scored['market_name']==name,'fire_risk_score'].iloc[0]); new=float(scen.fire_risk_score)
    x,y,z=st.columns(3); x.metric('Baseline score',f'{orig:.1f}'); y.metric('Scenario score',f'{new:.1f}',delta=f'{new-orig:+.1f}'); z.metric('Scenario level',str(scen.risk_level))

elif page == 'Data Upload':
    st.markdown('<div class="section-title">Data Upload</div><div class="section-sub">Upload local CSV files. Nothing is sent to external services.</div>', unsafe_allow_html=True)
    up1,up2=st.columns(2)
    with up1:
        f1=st.file_uploader('Upload market metrics',type=['csv'],key='metrics_upload')
        if f1:
            df=pd.read_csv(f1); ok,missing=validate_schema(df,REQUIRED_METRICS)
            if ok: st.session_state.metrics_df=df; st.success(f'Loaded {len(df)} market records.')
            else: st.error('Missing columns: '+', '.join(missing))
    with up2:
        f2=st.file_uploader('Upload inspection history',type=['csv'],key='history_upload')
        if f2:
            dfh=pd.read_csv(f2); ok,missing=validate_schema(dfh,REQUIRED_HISTORY)
            if ok: st.session_state.history_df=dfh; st.success(f'Loaded {len(dfh)} history records.')
            else: st.error('Missing columns: '+', '.join(missing))

elif page == 'Reports':
    st.markdown('<div class="section-title">Reports</div><div class="section-sub">Export transparent screening outputs for operational review.</div>', unsafe_allow_html=True)
    st.dataframe(scored.sort_values('fire_risk_score',ascending=False).head(15),width='stretch',hide_index=True)
    st.download_button('Download complete risk report',scored.to_csv(index=False).encode(),'firewatch_risk_report.csv','text/csv')
    priority=scored[scored['risk_level'].isin(['High','Critical'])].sort_values('fire_risk_score',ascending=False)
    st.download_button('Download priority queue',priority.to_csv(index=False).encode(),'firewatch_priority_queue.csv','text/csv')
    st.warning('Screening scores support inspection planning; they do not certify fire safety, compliance, or emergency readiness.')
