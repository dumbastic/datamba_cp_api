from django.contrib.auth.models import User, Group
from goers.models import Training, Recommendation
from rest_framework import viewsets
from goers.serializers import UserSerializer, GroupSerializer, TrainingSerializer, RecommendationSerializer

# Main ML library
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import psycopg2
import pandas as pd
from sqlalchemy import create_engine

import pickle

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    # LOAD DATA
    # Create connection to database    
    host = '157.230.240.246'
    port = '5432'
    username = 'iykra_trainee'
    password = 'passwordiykra'
    database = 'sandbox'

    engine = create_engine ('postgresql+psycopg2://'+username+':'+password+'@'+host+':'+port+'/'+database)
    df = pd.read_sql_query('select * from team5.z_user_tech_startup',con = engine)

    # SPLIT DATA
    train_pd, test_pd = train_test_split(df, test_size=0.2)

    # DATA PREPROCESSING
    train_pd_processed = pd.get_dummies(train_pd, columns=['gender','target'])

    feature_names = list(train_pd_processed.columns)
    do_not_use_for_training = ['user_id','gender','target','target_Others','target_Tech StArtup']

    feature_names = [f for f in train_pd_processed.columns if f not in ['user_id','gender','target','target_Others','target_Tech StArtup']]

    train_pd_processed[feature_names].count()
    target = train_pd_processed['target_Others']

    # TRAIN TEST
    Xtr, Xv, ytr, yv = train_test_split(train_pd_processed[feature_names].values, target, test_size=0.2, random_state=1897)

    # MODELING
    RF = RandomForestClassifier()
    RF.fit(Xtr, ytr)

    #trainPredict = RF.predict(Xtr)
    #obsPredict = RF.predict(Xv)
    
    # EVALUATION
    # Train Accuracy
    #RF.score(Xtr, ytr)

    # Test Accuracy
    #RF.score(Xv, yv)

    #df_confusion = pd.crosstab(yv, obsPredict, rownames=['Actual'], colnames=['Predicted'], margins=True)
    
    pickle.dump(RF, open("model", 'wb'))

    Training.objects.all().delete()
    Training.objects.create(algorithm="Random Forest", test_size=0.2, train_accuracy=RF.score(Xtr, ytr), test_accuracy=RF.score(Xv, yv))

    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        age = self.request.query_params.get('age')
        gender = self.request.query_params.get('gender')

        if (gender is not None and age is not None):
            gender = gender.upper()
        else:
            return None

        if (gender == "F" or gender == "M"):
            try: 
                int(age)
            except ValueError:
                return None
            try:
                model = pickle.load(open("model", 'rb'))
            except:
                

            prediction = model.predict([[age, 1 if gender=="F" else 0, 1 if gender=="M" else 0]])
            
            Recommendation.objects.all().delete()
            Recommendation.objects.create(prediction=prediction[0], description="Others" if prediction[0]==1 else "Tech Startup")

            return Recommendation.objects.all()
        else:
            return None
