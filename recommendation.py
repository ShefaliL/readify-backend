import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



def get_recommendations_list(book_id_list):

    #read all pickle files
    books_df,cm_author,cm_title_genre = get_count_matrix()
    
    
    #final_recommendations
    final_rec = []

    #iterate over input list
    for book_id_obj in book_id_list:
        book_id = book_id_obj['book_id']
        # print("rec book_id:",book_id)
        book = books_df[books_df.book_id == book_id][['book_id','book_title','book_author']].values[0]

        author_list = get_author_recomm(book, cm_author, books_df)
        title_genre_list = get_title_genre_recomm(book, cm_title_genre, books_df)

        # merge author and title_genre list
        recom_per_book = author_list + list(set(title_genre_list) -set(author_list))
        final_rec += list(set(recom_per_book) - set(final_rec))
       
    return final_rec

def get_recomm_for_book(book_id):
    #read all pickle files
    books_df,cm_author,cm_title_genre = get_count_matrix()

    book = books_df[books_df.book_id == int(book_id)][['book_id','book_title','book_author']].values[0]

    author_list = get_author_recomm(book, cm_author, books_df)
    title_genre_list = get_title_genre_recomm(book, cm_title_genre, books_df)




    if len(author_list) >=8:
         dup_author_list = author_list[:8]
    else: 
        dup_author_list = []+author_list

    remaining_count = 18-len(dup_author_list)

    recom_for_book = dup_author_list + list(set(title_genre_list) -set(author_list))[:remaining_count]

    return recom_for_book


def get_count_matrix():
    #book pickle --> book-dataframe
    books_pickle = pd.read_pickle('books_df2.pkl')
    books_df = books_pickle['books_df2']

    #Cm based on author
    author_pickle = pd.read_pickle('cm_author.pkl')
    cm_author = author_pickle['count_matrix']

    #Cm based on title,genre
    title_genre_pickle = pd.read_pickle('cm_title_genre.pkl')
    cm_title_genre = title_genre_pickle['count_matrix']   

    return books_df, cm_author,cm_title_genre

# def get_recom_cold_start(initial_genres):


def get_author_recomm(book, cm_author, books_df):

    #book pickle --> book-dataframe
    books_pickle = pd.read_pickle('books_df2.pkl')
    books_df = books_pickle['books_df2']
  

    #find similarity score for book
    cs_author = cosine_similarity(cm_author[book[0]-1],cm_author)

    #get score based on author
    author_scores = list(enumerate(cs_author[0]))

    #sort the score
    sorted_author_scores = sorted(author_scores, key=lambda x:x[1], reverse=True)

    #get recommendations based on author
    i = 0
    author_list = []
    for book_with_score in sorted_author_scores:
        temp_recomm = books_df[books_df.book_id == book_with_score[0]+1][['book_id','book_title','book_author']].values[0]
        if book[2] in temp_recomm[2] and book[0] != temp_recomm[0]:
            author_list.append(temp_recomm[0])
        i+=1
        if i>= 30:
            break

    return author_list

def get_title_genre_recomm(book, cm_title_genre, books_df):

    # print("finding books based on title, genre")

    #find similarity based on genre, title
    cs_title_genre = cosine_similarity(cm_title_genre[book[0]-1], cm_title_genre)

    #get score based on title and genre
    title_genre_score = list(enumerate(cs_title_genre[0]))

    #sort score
    sorted_title_genre_scores = sorted(title_genre_score, key=lambda x:x[1], reverse=True)


    # get recommendations based 
    j = 0
    title_genre_list = []
    for book_with_score in sorted_title_genre_scores:
        temp_recomm = books_df[books_df.book_id == book_with_score[0]+1][['book_id','book_title','book_rating','book_numratings']].values[0]
        if book[0] != temp_recomm[0] and temp_recomm[2]>=3.0 and temp_recomm[3]>=100:
            title_genre_list.append(temp_recomm[0])
        j+=1
        if j>=65:
            break

    return title_genre_list
    



# input_list = [{'book_id': 2}, {'book_id': 1}]
# recom = get_recommendations(input_list)
# print(recom)
