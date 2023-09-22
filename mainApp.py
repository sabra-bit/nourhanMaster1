import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import time
import plotly.figure_factory as ff
import pandas as pd
from streamlit_star_rating import st_star_rating
# st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ['home','add rating',"setting"], 
        icons=['house','list-task','gear'], menu_icon="cast", default_index=0)#cloud-upload

if selected =="setting":
    tab1, tab2 , tab3 ,tab4= st.tabs(["knowledge domain", "subject","view knowledge domain" ,"add organization"])
    with tab1:
        st.title("add knowledge domain/subject")
        st.markdown("""---""")
        st.subheader('add knowledge domain:')
        knowledge = st.text_input("enter knowledge domain name:")
        st.subheader('add knowledge domain prerequisite')
        st.caption('type (any) for no prerequisite and for  multi prerequisite split by - .' )
        st.caption('age must input range like 1-5.' )
        col1, col2= st.columns(2)
        
        with col1:
            degree = st.text_input('degree:')
            jop = st.text_input('jop:')
            age = st.text_input('age:')
            organization = st.text_input('organization:')
        with col2:
            sector = st.text_input('sector:')
            department = st.text_input('department:')
            unit = st.text_input('unit:')
            oldcourse = st.text_input('prerequisite course')
            
        if st.button("add knowledge domain") and knowledge and degree and jop and age and sector and department and unit  and organization and oldcourse:
            con = sqlite3.connect("data_store.db")                   
            cur = con.cursor()
            con.execute("create table if not exists knowledge  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgename TEXT NOT NULL, degree TEXT NOT NULL, jop TEXT NOT NULL , age TEXT NOT NULL , sector TEXT NOT NULL , department TEXT NOT NULL , unit TEXT NOT NULL, organization TEXT NOT NULL, oldcourse TEXT NOT NULL , active TEXT NOT NULL)")
            with sqlite3.connect("data_store.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into knowledge (knowledgename, degree, jop,age,sector,department,unit,organization,oldcourse,active) values (?,?,?,?,?,?,?,?,?,?)",(knowledge,degree,jop,age,sector,department,unit,organization,oldcourse,"True"))  
                con.commit()
                
            with st.empty():
                for seconds in range(3):
                    st.write(f"⏳ {seconds} seconds have passed")
                    time.sleep(1)
                st.write("✔️ saved!")  
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        cur.execute("select *  from knowledge;")
        result = cur.fetchall()
        if result:
            data_matrix = []
            data_matrix.append(['#','knowledge domain','degree','jop','age','sector','department','unit','organization','prerequisite' ,'is active'])
            # for i in result:
            #     data_matrix.append([i[0],i[2]])
            data_matrix = data_matrix+result
            # st.table(data_matrix)
            fig = ff.create_table(data_matrix)
                
            st.plotly_chart(fig)
    
    
    
    with tab2:        
        
        st.title("add knowledge domain/subject")
        st.markdown("""---""")
        st.subheader('add subject (courese):')
        
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        cur.execute("select id, knowledgename  from knowledge  ;")
        result = cur.fetchall()
        modules = []
        for i in result:
            modules.append(str(i[1]))
        option = st.selectbox(
        'selecte knowledge domain:',modules)
        
        subjectName=st.text_input('subject name:')
        col1, col2= st.columns(2)
        
        with col1:
            typ = st.radio("Study method :",['any',"online", "off line"] , horizontal=True)
            joplevel = st.text_input('jop level:')
            ageRange = st.text_input('age range:')
        with col2:
            degree = st.text_input('degree: ')
            courseHouer = st.text_input('course Houer:')
            oldcourse = st.text_input('prerequisite course:')
        if st.button("add subject"):
            if option and subjectName:
                con = sqlite3.connect("data_store.db")                   
                cur = con.cursor()
                con.execute("create table if not exists subject  (id INTEGER PRIMARY KEY AUTOINCREMENT, subjectName TEXT NOT NULL, knowledgename TEXT NOT NULL, typeS TEXT NOT NULL ,joplevel TEXT NOT NULL , ageRange TEXT NOT NULL , degree TEXT NOT NULL , courseHouer TEXT NOT NULL ,oldcourse TEXT NOT NULL)")
                with sqlite3.connect("data_store.db") as con:  
                    cur = con.cursor()  
                    cur.execute("INSERT into subject (subjectName, knowledgename ,typeS ,joplevel ,ageRange ,degree,courseHouer ,oldcourse) values (?,?,?,?,?,?,?,?)",(subjectName,option,typ,joplevel,ageRange,degree,courseHouer,oldcourse))  
                    con.commit()
                with st.empty():
                    for seconds in range(3):
                        st.write(f"⏳ {seconds} seconds have passed")
                        time.sleep(1)
                    st.write("✔️ saved!")
        
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        cur.execute("select *  from subject  ;")
        result = cur.fetchall()
        if result:
            data_matrix = []
            data_matrix.append(['#','subject','knowledge domain'])
            for i in result:
                data_matrix.append([i[0],i[1],i[2]])
            fig = ff.create_table(data_matrix)
                
            st.plotly_chart(fig)
    with tab3:
        
    

        st.title("view  knowledge domain/subject")
        st.markdown("""---""")
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        subject = cur.execute("select *  from subject  ;")
        subject = subject.fetchall()
        module = cur.execute("select *  from knowledge  ;")
        module = module.fetchall()
        for mod in module:
            st.subheader(mod[1])
            st.write('prerequisite:')
            st.write('state: '+str(mod[10]))
            col1, col2= st.columns(2)
            
            with col1:
                st.write('degree: '+str(mod[2]))
                st.write('jop: '+str(mod[3]))
                st.write('age: '+str(mod[4]))
                st.write('organiztion : '+str(mod[8]))
            with col2:
                st.write('sector: '+str(mod[5]))
                st.write('department: '+str(mod[6]))
                st.write('unit: '+str(mod[7]))
                st.write('prerequisite course: '+str(mod[9]))
            st.write('subject:')    
            for sub in subject:
                if sub[2] == mod[1]:
                    st.text(sub[1] + " with prerequisite " +sub[8] + " and type of stude "+ sub[3] )
            st.markdown("""---""") 
            
    with tab4: 
               

        st.subheader('add organization')
        organizatin = st.text_input('organizatin:')
        sector = st.text_input('sector: ')
        department = st.text_input('department: ')
        unit = st.text_input('unit: ')
        if st.button("add") and organizatin and sector and department and unit :
            con = sqlite3.connect("data_store.db")                   
            cur = con.cursor()
            con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
            with sqlite3.connect("data_store.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into organization (organizationName,sector,department,unit) values (?,?,?,?)",(organizatin,sector,department,unit))  
                con.commit()
            with st.empty():
                for seconds in range(3):
                    st.write(f"⏳ {seconds} seconds have passed")
                    time.sleep(1)
                st.write("✔️ add!")
        
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        org = cur.execute("select *  from organization  ;")
        org = org.fetchall()
        
        for mod in org:
            
            st.write(mod[1])
        
    
if selected =="home":
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    org = cur.execute("select *  from organization  ;")
    org = org.fetchall()
    orgainzation =[]
    for mod in org:
        orgainzation.append(mod[1])
     
    col1, col2= st.columns(2)
    with col1:
        organiz = st.selectbox('organization: ',orgainzation) 
        sector = st.text_input('sector:')
        department = st.text_input('department:')
        unit = st.text_input('unit:') 
        job = st.text_input('job:')
        
    with col2:
        degree = st.text_input('degree:')
        age = st.text_input('age:')
        oldCourse = st.text_input('old subject (course):')
        
     
    st.caption('old subject (course) must separeted with (-) .')   
    active = st.checkbox('custum plan')
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    org = cur.execute("select *  from subject  ;")
    org = org.fetchall()
    subject =[]
    for mod in org:
        subject.append(mod[1])
    subj = st.multiselect('select custum subject: ',subject,disabled = (not active))
    
    df1 = pd.DataFrame()
    
    if 'plane' in  st.session_state:
        df1 = st.session_state['plane']
    else:
        st.session_state['plane'] = df1  
    for sub in org:
        if  sub[1] in subj  :
            if 'any' in sub[8] :
                st.success('allowed', icon="✅")
                st.write(sub[2])
                st.write('course :blue['+sub[1]+'] ' +'with '+sub[7] +' H')
                df1 = df1.append({
                    "knowlge":sub[2] ,
                    "course": sub[1],
                    "houer" :sub[7],
                    "prerequisite":"any"
                    } , ignore_index=True)
                st.session_state['plane'] =  df1.append( st.session_state['plane'], ignore_index=True)
            else:
                st.warning('prerequisite needed', icon="⚠️")
                st.write(sub[2])
                st.write('course :blue['+sub[1]+'] ' +'with '+sub[7] +' H')
                st.write(':red[prerequisite] needed is : ' + sub[8])
                df1 = df1.append({
                    "knowlge":sub[2] ,
                    "course": sub[1],
                    "houer" :sub[7],
                    "prerequisite":sub[8]
                    } , ignore_index=True)
                st.session_state['plane'] =  df1.append( st.session_state['plane'], ignore_index=True)
    df1 = pd.DataFrame()
    if 'plane' in  st.session_state:
        df1 = st.session_state['plane']
    else:
        st.session_state['plane'] = df1 
    if st.button("auto genrate plane") :
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        cur.execute("select *  from knowledge where active = 'True' ;")
        result = cur.fetchall()
        plan = []
        
        for i in result:
            if (organiz in i[8] or 'any'in i[8]) and (sector in i[5] or 'any'in i[5]) and (department in i[6] or 'any'in i[6]) and (unit in i[7] or 'any'in i[7])  and (job in i[3] or 'any'in i[3]) and (degree in i[2] or 'any'in i[2]) and ((age >= i[4].split('-')[0] and age <= i[4].split('-')[1] ) or 'any'in i[4]) and ((set(oldCourse.split('-')).issubset(set(i[9].split('-')))) or 'any'in i[9]):
                
                
                
                subject = cur.execute("select *  from subject  ;")
                subject = subject.fetchall()
                st.subheader("Recommended knowledge domain: "+i[1])
                st.write("subject:")
                for sub in subject:
                    if sub[2] == i[1]:
                        if 'any' in sub[8] or set(oldCourse.split('-')).issubset(set(sub[8].split('-')))  :
                            st.write('course :blue['+sub[1]+'] ' +'with '+sub[7] +' H')
                            df1 = df1.append({
                                "knowlge":sub[2] ,
                                "course": sub[1],
                                "houer" :sub[7],
                                "prerequisite":'any'
                                } , ignore_index=True)
                        else:
                            st.write('course :blue['+sub[1] +']'+'with '+sub[7] +' H'+' need :red['+ sub[8] +'] first')
                            df1 = df1.append({
                                    "knowlge":sub[2] ,
                                    "course": sub[1],
                                    "houer" :sub[7],
                                    "prerequisite":sub[8]
                                    } , ignore_index=True)
        
        
        st.session_state['plane'] =  df1.append( st.session_state['plane'], ignore_index=True)
        st.toast('plane genrated!', icon='🎉')
    if 'plane' in  st.session_state:
         if st.button("delete old plane")  :
             del st.session_state['plane']
    if st.button("view plane")  :
        df_plane = st.session_state['plane'].drop_duplicates()
        print (df_plane)     
        st.dataframe(df_plane) 
    uploaded_file = st.file_uploader("upload trainee data")
    if uploaded_file is not None:
        dfUpload = pd.read_excel(uploaded_file)
    
if selected =="add rating":
    stars = st_star_rating("Please rate you experience", maxValue=5, defaultValue=3, key="rating") 
    print(stars) 
    st.write(stars)
    