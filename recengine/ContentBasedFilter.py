import numpy as np
import scipy
import pandas as pd
import sklearn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedFilter:
    def __init__(self, app_payload):
        self.generatedList = app_payload['newRecipes']
        self.userData = app_payload['user']
        self.stopwords_list = stopwords.words('english')
        self.vectorizer = TfidfVectorizer(analyzer='word',
                            ngram_range=(1, 2),
                            min_df=0.003,
                            max_df=0.5,
                            max_features=1000,
                            stop_words=self.stopwords_list)
        self.tfidf_matrix = ''
        self.tfidf_feature_names = ''
        self.concat_titles_summaries = []
        self.user_recipe_ids = []
        self.all_recipe_ids = []
        self.recipe_ratings = []
        self.userprofile = ''
        self.__gib_user_profile()

    def __populate_lists(self):
        for recipe in self.userData:
            self.concat_titles_summaries.append(recipe['title'] + recipe['summary'])
            self.user_recipe_ids.append(recipe['id'])
            self.all_recipe_ids.append(recipe['id'])
            self.recipe_ratings.append(recipe['rating'])
        for recipe in self.generatedList:
            self.concat_titles_summaries.append(recipe['title'] + recipe['summary'])
            self.all_recipe_ids.append(recipe['id'])

    def __generate_tf_idf(self):
        self.tfidf_matrix = self.vectorizer.fit_transform(self.concat_titles_summaries)
        self.tfidf_feature_names = self.vectorizer.get_feature_names()

    def __get_recipe_profile(self, id):
        idx = self.all_recipe_ids.index(id)
        recipe_profile = self.tfidf_matrix[idx:idx+1]
        return recipe_profile

    def __get_recipe_profiles(self, ids):
        recipe_profiles_list = [self.__get_recipe_profile(x) for x in ids]
        recipe_profiles = scipy.sparse.vstack(recipe_profiles_list)
        return recipe_profiles

    def __build_users_profile(self):
        user_recipe_profiles = self.__get_recipe_profiles(self.user_recipe_ids)
        user_recipe_strengths = np.array(self.recipe_ratings).reshape(-1, 1)
        user_recipe_strengths_weighted_avg = np.sum(user_recipe_profiles.multiply(user_recipe_strengths),
                                                    axis=0) / np.sum(user_recipe_strengths)
        user_profile_norm = sklearn.preprocessing.normalize(user_recipe_strengths_weighted_avg)
        return user_profile_norm

    def __gib_user_profile(self):
        self.__populate_lists()
        self.__generate_tf_idf()
        self.userprofile = self.__build_users_profile()
        # d = pd.DataFrame(sorted(zip(self.tfidf_feature_names, self.userprofile.flatten().tolist()),
        #                        key=lambda x: -x[1])[:20],
        #                 columns=['token', 'relevance'])

    def __get_similar_recipes_to_user(self, topn=20):
        cosine_similarities = cosine_similarity(self.userprofile, self.tfidf_matrix)

        similar_indices = cosine_similarities.argsort().flatten()[-topn:]

        similar_recipes = sorted([(self.all_recipe_ids[i], cosine_similarities[0, i]) for i in similar_indices],
                                 key=lambda x: -x[1])
        return similar_recipes

    def __recommend_recipes(self, recipes_to_ignore=[], topn=5):
        similar_recipes = self.__get_similar_recipes_to_user()
        similar_recipes_filtered = list(filter(lambda x: x[0] not in recipes_to_ignore, similar_recipes))
        # Debug stuff
        rec_df = pd.DataFrame(similar_recipes_filtered, columns=['id', 'strength']).head(topn)
        rec_df_json = rec_df.to_json(orient='records')
        return rec_df_json

    def get_recommendation(self):
        message = self.__recommend_recipes(recipes_to_ignore=self.user_recipe_ids)

        return message
