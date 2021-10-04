import streamlit as st
import pandas as  pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import re
st.set_page_config(layout="wide")



##### loading data 

@st.cache
def fetch_and_clean_data():
    df =  pd.read_csv('vulnerabilities.csv')
    df.date_detected = pd.to_datetime(df['date_detected']).dt.date
    date_lst = list(df.date_detected.unique())
    date_lst.sort(reverse=True)

    return df, date_lst

df, date_lst = fetch_and_clean_data()


st.title("Security Dashboard")
analysis_dt = st.selectbox('Select Analysis Date', date_lst)

error_cat = ['sql injection','cookies present without secure flag','private ip in html', 'http parameter override', 'cross domain javascript source file present']

def detect_type(bug):
    bug = ' '.join(re.sub(r'[^a-z ]', ' ',  bug.lower()).split())
    match_flg = [len(list(set(i.split()).intersection(bug.split()))) for i in error_cat]
    if max(match_flg) > 0:
        bug_type = error_cat[match_flg.index(max(match_flg))]
    else:   
        match_cnt = [len(list(set(i.split()).intersection(bug.split())))  for i in error_cat]
        bug_type = error_cat[match_cnt.index(max(match_flg))]
    return bug_type


df = pd.melt(df,id_vars=['date_detected'],var_name=['source'], value_name='vulnerability').dropna()
df['vulnerability_type']= df['vulnerability'].apply(lambda x: detect_type(x))

#df1 = df.groupby('source')['vulnerability'].apply(list).reset_index(name='similar_describtion')
#df['date_detected'] = df['date_detected'].apply(lambda x: x.strftime("%Y-%mm-%dd, %H:%M:%S") )


df1 = df.groupby(['vulnerability_type'], as_index=False)['vulnerability','date_detected','source'].agg(lambda x: list(set(x)))

a =df1[df1.vulnerability_type.isin(df[df.date_detected == analysis_dt]['vulnerability_type'])]
a['is_new'] = a.date_detected.apply(lambda x: len(x)<2 or min(x) == analysis_dt)

#print(('\n').join(['a','b','c']))

a['date_detected'] = a['date_detected'].apply(lambda x: (""";          \n""").join(j.strftime("%Y-%m-%d") for j in x ))
a['vulnerability'] = a['vulnerability'].apply(lambda x: (";          \n").join(j for j in x ))
a['source'] = a['source'].apply(lambda x: (";          \n").join(j for j in x ))


a.columns = ['Vulnerability', 'Possible Descriptions', 'Observation Dates', 'Sources', 'Is New']
a = a[['Vulnerability',  'Sources', 'Is New', 'Observation Dates','Possible Descriptions']]
#a['date_detected'] = (', \n').join(['aaa','bbbbb','cbbbb'])
#bug = 'Cross-Domain JavaScript Source File Inclusion Cross-Domain JavaScript Source File Inclusion '


#analysis_dt
    
#temp = df[df.date_detected == analysis_dt].sort_values(by=['date_detected'])
    
#temp = df[df.date_detected == analysis_dt].sort_values(by=['date_detected']).drop_duplicates(subset=['vulnerability_type','source'], keep = 'first').loc[:, [ 'source', 'vulnerability', 'vulnerability_type']].reset_index().drop('index', axis = 1)
#st.dataframe(a)
#st.table(a)

AgGrid(a)





# option = st.selectbox(
# ...     'How would you like to be contacted?',
# ...     ('Email', 'Home phone', 'Mobile phone'))


# st.session_state.clb_nbr = st.selectbox('Select Club Number', list(df.club_nbr.unique()))
# st.session_state.wght= st.slider("Enter Sales Contribution (Membership Contribution = 100 - Sales Contribution)",value = 88, min_value=0, max_value=100)
# st.session_state.capacity = int(df_capacity[df_capacity.club_nbr == st.session_state.clb_nbr].total_pal.iloc[0])

# st.session_state.df = df.query("club_nbr == @st.session_state.clb_nbr").loc[:,['category_nbr', 'n_pal' , 'se_member', 'se_sales']].copy()
# st.session_state.df = pd.melt(st.session_state.df, id_vars=['category_nbr','n_pal'], value_vars=['se_member', 'se_sales'], var_name='measure_name', value_name='measure').copy()
# df_cat_temp = df_cat.query("club_nbr == @st.session_state.clb_nbr").loc[:,['category_nbr', 'n_palamax' , 'n_palamin']].copy()

# #st.session_state. 
# #st.session_state.
# #######################################################
# #df_cat_temp = df_cat[df_cat.club_nbr == clb_nbr]
# #st.session_state.flag = False


# def optimize():
#     # if 'df_cat' in st.session_state:
#     #     st.dataframe(st.session_state.df_cat)
#     fract_dict = {'se_member': 0.5106788995796772, 'se_sales': 0.48932110042032284}
#     weight = {'se_sales':st.session_state.wght, 'se_member':(100 -st.session_state.wght)}
    
#     input_df_temp = (st.session_state.df
#                      .assign(measure=st.session_state.df[['measure','measure_name']].groupby('measure_name').transform(lambda x: x / x.sum())
#                                                                          .loc[:,'measure']  * (st.session_state.df.measure_name.map(weight))   *  (st.session_state.df.measure_name.map(fract_dict)) ) 
#                      .drop('measure_name', 1)
#                     ).copy()

#     #summing up measures per category per club
#     input_df_temp = (input_df_temp.groupby(['category_nbr', 'n_pal'], as_index=False)[["measure"]].sum()).copy()

#     #display(input_df_temp)

#     mat = (input_df_temp.assign(ind=1)
#                .pivot(columns = 'category_nbr', values = 'ind')
#                .rename_axis(None, axis = 'columns')
#                .transpose()
#                .fillna(0)
#                .to_numpy()
#                )  
#     nrow = input_df_temp.shape[0]





#     model = pyo.ConcreteModel()
#     model.x = pyo.Var(range(nrow), domain= pyo.Binary)

#     model.constraints = pyo.ConstraintList()
#     for arow in mat:
#       model.constraints.add( pyo.summation(arow , model.x) == 1)
#     model.constraints.add(  pyo.summation(list(input_df_temp['n_pal']) , model.x) <= st.session_state.capacity)
#     model.obj_sales = pyo.Objective(expr =  pyo.summation(list(input_df_temp['measure']), model.x), sense = pyo.maximize) 
#     results =  SolverFactory('glpk').solve(model)

#     solution = [model.x[j].value for j in range(nrow)]
#     df_sol = (input_df_temp.loc[:, ['category_nbr', 'n_pal']]
#                              .assign(solution = solution)
#                              .query('solution == 1')
#                              .drop(columns = 'solution')
#                              .rename(columns = {'n_pal': 'n_pal_opt'})
#                    )
    
#     #df_sol.index = [""] * len(df_sol)
#     gb = GridOptionsBuilder.from_dataframe(df_sol)
    
#     AgGrid(df_sol)

#     #st.dataframe(df_sol)






# def foo():
#     if st.button('Edit Constraints'):
#         st.session_state.flag = True
#         edit_constraints()
#     if st.button('Optimize'):
#          optimize()


    
# def edit_constraints():
#     if st.button('Review Optimization'):
#         del st.session_state['flag']
#         foo()
#         return 0

#     st.subheader('Capacity')
#     st.session_state.capacity = st.slider("Capacity ", min_value=1000, max_value=2000, value=st.session_state.capacity  )




#     lst = []
#     st.subheader('Mimimum/Maximum pallet count for each category')

#     for i in list(df_cat_temp.category_nbr.unique()):
#         c, d = st.slider("Category "+str(i),value = [int(df_cat_temp.query(" category_nbr == {}".format(int(i))).n_palamin.iloc[0]),int(df_cat_temp.query(" category_nbr == {}".format(int(i))).n_palamax.iloc[0])])
#         lst.append([i,c,d])    
#     st.session_state.df_cat = pd.DataFrame(lst, columns =['Category', 'n_pal_min', 'n_pal_max'])





# # PAGES = {
# #     "App1": foo,
# #     "Edit Constrains": edit_constraints
# # }

# #st.sidebar.title('Navigation')

# #selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# # page = PAGES[selection]

# # page()
# if 'flag' not in st.session_state:
#     foo()
# else:
#     edit_constraints()