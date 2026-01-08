import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from numerize.numerize import numerize
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
 
st.set_page_config(
    page_title='Dashboard',
    page_icon='📈',
    layout='wide'
)

# Load configuration from YAML file
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
 
# Initialize Streamlit Authenticator with configuration settings
# Initialize Streamlit Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
# Perform user authentication

 
# Check if the user is authenticated
if not st.session_state.get("authentication_status"):
    st.info('Please log in to access the application from the MainPage.')
else:
   def main():
    
    # Access data from session state
    data = st.session_state.get("data_key", None)
    # Check if the user is authenticated
    if data is None:
     st.info('Please Kindly Access the DataPage to Configure your DataSet.')
     
    else: 
      
      table_feature = data.columns.tolist()
      
      churn_rate = (data["CHURN"].sum() / data.shape[0]) * 100
      On_net_calls = data['ON_NET'].sum()
      average_MONTANT_charges = data['MONTANT'].mean()
      total_revenue = data['REVENUE'].sum()
      total_Users = data['TENURE'].count()


      if data is not None:
         
            with st.container():
                        
                                 #3. columns
                  total1,total2,total3,total4,total5 = st.columns(5,gap='small')
                  with total1:

                     st.info('On_Net Sum', icon="🔍")
                     st.metric(label = '', value= f"{On_net_calls:,.0f}")
                     
                  with total2:
                     st.info('Avg_Montant', icon="🔍")
                     st.metric(label='', value=f"{average_MONTANT_charges:,.0f}")

                  with total3:
                     st.info('Total Rev', icon="🔍")
                     st.metric(label= '',value=f"{total_revenue:,.0f}")

                  with total4:
                     st.info('No_of_Users', icon="🔍")
                     st.metric(label='',value=f"{total_Users:,.0f}")

                  with total5:
                     st.info('Churn Rate', icon="🔍")
                     st.metric(label='',value=numerize(churn_rate),help=f"""Total rating: {churn_rate}""")
      
                  st.markdown("""---""")

                                    
      
         
            
      
         
            with st.container():
                     
                     data_df= data
                     data_df.columns.tolist()

                     cpp1, cpp2 = st.columns(2)
                     with cpp1:
                        st.title('Univariate Analysis')
                     with cpp2:
                           #selected_uni_feature = st.selectbox('Select Feature', data_df)
                           selected_feature=st.selectbox('Select a Feature', options=table_feature, key='selected_model')

                     co1, co2 = st.columns(2)
                                    
                     with co1:
                           fig = px.histogram(data, x=selected_feature, color=selected_feature, barmode="group", height=400, width=500)
                           fig.update_yaxes(title_text=None)
                           st.plotly_chart(fig)
   
                     with co2:
                           fig = px.box(data, x=selected_feature, height=400, width=500)
                           st.plotly_chart(fig)
            with st.container():
                     st.title('Churn rate: For Per Selected Features')           

                     cn1, cn2 = st.columns(2)
                     
                     with cn1:
                           fig = px.histogram(data, x=selected_feature, height=400, width=500)
                           fig.update_yaxes(title_text=None)
                           st.plotly_chart(fig)
   
                     with cn2:
                           senior_citizen_pie = px.pie(data, names=selected_feature, color=selected_feature)
                           st.plotly_chart(senior_citizen_pie, use_container_width=True)
                        
            with st.container():
                     cppo1, cppo2, cppo3= st.columns(3)
                     with cppo1:
                        st.title('Bivariate  Analysis')
                     with cppo2:
                           #selected_uni_feature = st.selectbox('Select Feature', data_df)
                           selected_feature1=st.selectbox('Select a Feature', options=table_feature, key='selected_modeli')
                     with cppo3:
                           #selected_uni_feature = st.selectbox('Select Feature', data_df)
                           selected_feature2=st.selectbox('Select a Feature', options=table_feature, key='selected_modela')
                     c1, c2 = st.columns(2)
                  
                     with c1:
                           sns.histplot(data, x=selected_feature1, hue=selected_feature1, multiple="stack")
   
                     with c2:
                           sns.histplot(data, x=selected_feature2, hue=selected_feature2, multiple="stack")
                                           
            with st.container():
                        df1 = data.drop(columns=['REGION', 'TENURE'])
                     
                        qppo1, qppo2, qppo3, qppo4, qppo5, qppo6 = st.columns(6)
                        with qppo1:
                           st.header('Multivariate')
                        with qppo2:
                           pass
                        with qppo3:
                           pass   
                        with qppo4:
                           z_variable = st.selectbox("Par1:", df1.columns)  
                        with qppo5:
                           x_variable = st.selectbox("Par2:", df1.columns)
                        with qppo6:
                           y_variable = st.selectbox("Par3:", df1.columns)    
                     
                     
                        ca1, ca2 = st.columns(2)
                        correlation_matrix = df1.corr(numeric_only=True)
                     
                        with ca1:  
                        
                         plt.figure(figsize=(10, 8))
                         sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
                         plt.title("Correlation Matrix")
                         st.pyplot(plt)
                           
   
                        with ca2:
               
                                 # Create 3D scatterplot
                           fig = plt.figure(figsize=(10, 8))
                           ax = fig.add_subplot(111, projection='3d')
                           ax.scatter(df1[x_variable], df1[y_variable], df1[z_variable])
                           ax.set_xlabel(x_variable)
                           ax.set_ylabel(y_variable)
                           ax.set_zlabel(z_variable)
                           ax.set_title("3D Scatter Plot") # Fixed: Set title on the axes object
                        
                           st.pyplot(fig)
                           
   if __name__ == '__main__':
              main()