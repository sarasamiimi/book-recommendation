from django.shortcuts import render
import pandas as pd
from . models import Book
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from .forms import Booksearchform

def loadbooks(BooksDataset):
 df= pd.read_csv(BooksDataset)
 return df


def creatbook():
    book_df =loadbooks('BooksDataset.csv')   

    for _, row in book_df . iterrows():
        Book.objects.get_or_create(title=row['Title'], author=row['Authors'], description=['Description']) 





# تابع برای ایجاد ماتریس TF-IDF
def create_tfidf_matrix():
    books = Book.objects.all()  # دریافت تمامی کتابها
    titles = [book.title for book in books]  # استخراج عناوین کتابها
    tfidf_vectorizer = TfidfVectorizer()  # ایجاد مدل وکتورایز
    tfidf_matrix = tfidf_vectorizer.fit_transform(titles)  # وکتورایز کردن عناوین
    return tfidf_matrix, tfidf_vectorizer  # 



# تابع برای ایجاد مدل KNN
def create_knn_model(tfidf_matrix):
    knn = NearestNeighbors(n_neighbors=3, metric='cosine')  # تنظیم تعداد همسایگان
    knn.fit(tfidf_matrix)  # آموزش مدل KNN بر روی ماتریس TF-IDF
    return knn 




def recommend_books(book_title):
    print(f"book:{book_title}")
    books = Book.objects.all()  # دریافت تمامی کتابها

    tfidf_matrix, tfidf_vectorizer = create_tfidf_matrix()  # ایجاد ماتریس TF-IDF
    knn_model = create_knn_model(tfidf_matrix)  # ایجاد مدل KNN

    try:
        # پیدا کردن ایندکس کتاب ورودی
        idx = next(i for i, book in enumerate(books) if book.title == book_title)
        distances, indices = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=7)  # پیدا کردن همسایگان نزدیک

        recommended_books = []
        for i in indices.flatten():
            recommended_books.append(books[int(i)])  # اضافه کردن کتابهای پیشنهادی به لیست
    
        return recommended_books  # بازگرداندن لیست کتابهای پیشنهادی
    except StopIteration:
        return None  




def index(request):
    form = Booksearchform()
    recommendations = []

    if request.method == 'POST':
        form = Booksearchform(request.POST)
        if form.is_valid():
            print("form is valid")
            book_title = form.cleaned_data['book_title'].strip()
            print(f"book title submited:{book_title}")
            recommendations = recommend_books(book_title)
            print(f"recommention returned : {recommendations}")

    return render(request, 'book/index.html', {'form': form, 'recommendations': recommendations})

     
