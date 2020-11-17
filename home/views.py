from django.shortcuts import render,redirect
from django.db import connection
import re
from django.http import HttpResponse
# Create your views here.

logged_in = False
ID = -1

def home_notLoggedIn(response):
    error_msg = ""
    no_of_results = ""
    if response.session.get('is_logged_in',False) == True:
        #return HttpResponse('This is User_ID' + request.session.get('user_ID',-1))
        id = response.session.get('user_ID', -1)
        show_list = []

        #search function
        if response.method == "POST":
            print("here")
            if response.POST.get("search_button") == "clicked":
                print(response.POST)
                search_item = response.POST.get('search_field')
                search_item = search_item.replace(" ","")
                search_pattern = "%" + search_item.lower() + "%"

                print(search_pattern)


                #search_type = response.POST.get('type')
                search_genre = response.POST.get('genre')
                search_lang = response.POST.get('language')
                search_from = response.POST.get('from_year')
                search_to = response.POST.get('to_year')

                #print(search_type)
                print(search_genre)
                print(search_lang)
                print(search_from)
                print(search_to)



                cursor = connection.cursor()
                sql = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s,ACTOR a,ACT ac" \
                      " WHERE s.SHOW_ID = ac.SHOW_IDACT AND ac.ACTOR_IDACT = a.PERSON_ID AND" \
                      " regexp_replace(LOWER(a.ACTOR_FIRST_NAME || ' ' || a.ACTOR_LAST_NAME), ' ','') like (%s)" \
                      " UNION" \
                      " (SELECT DISTINCT(s.SHOW_ID) FROM SHOW s, SERIES se"\
                      " WHERE s.SERIES_ID = se.SERIES_ID" \
                      " AND s.SEASON_NO = se.SEASON_NO" \
                      " AND regexp_replace(LOWER(se.TITLE), ' ','') like (%s)" \
                      " )" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT(s.SHOW_ID)" \
                      " FROM SHOW s, DIRECTOR d" \
                      " WHERE s.DIRECTOR_ID = d.PERSON_ID" \
                      " AND regexp_replace(LOWER (d.DIRECTOR_FIRST_NAME || ' ' || d.DIRECTOR_LAST_NAME), ' ','') like (%s)" \
                      " )" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT(s.SHOW_ID) FROM SHOW s" \
                      " WHERE regexp_replace(LOWER(s.TITLE), ' ','') like (%s)" \
                      " OR regexp_replace(LOWER(s.GENRE), ' ','') like (%s)" \
                      " )"

                cursor.execute(sql,[search_pattern,search_pattern,search_pattern,search_pattern,search_pattern])
                result = cursor.fetchall();
                cursor.close()

                print(type(result))


                search_genre = response.POST.get('genre')
                search_genre = search_genre.replace(" ", "")
                search_genre = "%" + search_genre.lower() + "%"
                print(search_genre)

                search_lang = response.POST.get('language')
                search_lang = search_lang.replace(" ", "")
                search_lang = "%" + search_lang.lower() + "%"

                print(search_lang)

                search_from = response.POST.get('from_year')

                print(search_from)

                search_to = response.POST.get('to_year')

                print(search_to)

                result_final = []


                result_genre = []
                if search_genre != "":
                    cursor = connection.cursor()
                    sql_genre = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s" \
                                " where regexp_replace(LOWER(s.GENRE), ' ','') Like (%s)"
                    cursor.execute(sql_genre, [search_genre])
                    result_genre = cursor.fetchall()
                    cursor.close()
                else:
                    result_genre = result

                result_lang = []
                if search_lang != "":
                    cursor = connection.cursor()
                    sql_lang = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s" \
                                " WHERE regexp_replace(LOWER(s.LANGUAGE), ' ','') Like (%s)"
                    cursor.execute(sql_lang, [search_lang])
                    result_lang = cursor.fetchall()
                    cursor.close()
                else:
                    result_lang = result

                result_from = []
                if search_from != "":
                    cursor = connection.cursor()
                    sql_from = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s where s.YEAR >= %s"
                    cursor.execute(sql_from, [search_from])
                    result_from = cursor.fetchall()
                    cursor.close()
                else:
                    result_from = result

                result_to = []
                if search_to != "":
                    cursor = connection.cursor()
                    sql_to = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s where s.YEAR <= %s"
                    cursor.execute(sql_to, [search_to])
                    result_to = cursor.fetchall()
                    cursor.close()
                else:
                    result_to = result

                result_temp = set(result_genre).intersection(set(result_from).intersection(result_to))
                result_temp_new = set(result_temp).intersection(set(result_lang))
                result_final = set(result).intersection(result_temp_new)


                error_msg = "No Result Found!"
                show_list=[]


                cnt = 0
                for r in result_final:
                    cnt = cnt+1
                    print(type(r))
                    show_id = r[0]
                    print(show_id)
                    cursor = connection.cursor()
                    sql = "SELECT * FROM SHOW WHERE SHOW_ID = %s"
                    cursor.execute(sql, [show_id])
                    show_res = cursor.fetchall()
                    cursor.close()
                    print("here")

                    for r_temp in show_res:
                        show_title = r_temp[2]
                        show_genre = r_temp[1]
                        show_des = r_temp[3]
                        show_age = r_temp[4]
                        show_lang = r_temp[8]
                        show_image = r_temp[13]
                        show_imdb = r_temp[5]
                        single_row = {"show_imdb": show_imdb,
                                      "show_title": show_title,
                                      "show_genre": show_genre,
                                      "show_des": show_des,
                                      "show_age": show_age,
                                      "show_lang": show_lang,
                                      "show_image": show_image}
                        show_list.append(single_row)
                        error_msg = ""
                no_of_results = str(cnt)

        else:
            cursor = connection.cursor()
            sql = "SELECT * FROM USERS WHERE USER_ID = %s"
            cursor.execute(sql, id)
            result = cursor.fetchall()
            cursor.close()
            for r in result:
                first_name = r[2]
            cursor = connection.cursor()
            sql = "SELECT * FROM SHOW"
            cursor.execute(sql)
            result_show = cursor.fetchall()
            cursor.close()
            show_list = []
            cnt = 0
            for r in result_show:
                cnt = cnt+1
                show_title = r[2]
                show_genre = r[1]
                show_imdb = r[5]
                show_image = r[13]
                single_row = {"show_title": show_title, "show_genre": show_genre, "show_imdb": show_imdb,
                              "show_image": show_image}
                show_list.append(single_row)
            no_of_results = str(cnt)

        return render(response, "home/homepage.html", {'no_of_results': no_of_results, 'shows': show_list, 'error_msg': error_msg})

    else:
        return redirect("http://127.0.0.1:8000/user/login")

#not used anymore, might use in future
def home_LoggedIn(request,user_ID):
    #Home page specific to user
    print(user_ID)

    if 'is_logged_in' in request.session:
        if user_ID == request.session.get('user_ID',-1) and request.session.get('is_logged_in', False) == True:
            #return HttpResponse('This is User_ID' + str(user_ID))
            return render(request,"home/homepage.html")
        else:
            print("not logged in")
            return redirect("http://127.0.0.1:8000/user/login/")

    else:
        print("not logged in")
        return redirect("http://127.0.0.1:8000/user/login/")


def log_out(request):
    if request.session.get('is_logged_in',False) == True:
        try:
            del request.session['user_ID']
            del request.session['is_logged_in']
        except KeyError:
            pass
        print("logged out successfully")

    return redirect("http://127.0.0.1:8000/user/login")


def genre(response, genre_name):
    if response.session.get('is_logged_in', False) == True:
        cursor = connection.cursor()
        genre_name = genre_name.lower()
        genre_pattern = "%"+genre_name+"%"
        print(genre_pattern)

        if genre_name != "miscellaneous":
            sql = "SELECT * FROM SHOW s WHERE lower(s.GENRE) LIKE %s"
            cursor.execute(sql, [genre_pattern])
        else:
            sql = "SELECT * FROM SHOW s"
            cursor.execute(sql)

        result = cursor.fetchall()
        cursor.close()

        show_list = []

        error_msg = "NO RESULT FOUND"
        cnt = 0
        for r_temp in result:
            cnt = cnt+1
            show_title = r_temp[2]
            show_genre = r_temp[1]
            show_des = r_temp[3]
            show_age = r_temp[4]
            show_lang = r_temp[8]
            show_image = r_temp[13]
            show_imdb = r_temp[5]
            single_row = {"show_imdb": show_imdb,
                            "show_title": show_title,
                          "show_genre": show_genre,
                          "show_des": show_des,
                          "show_age": show_age,
                            "show_lang": show_lang,
                          "show_image": show_image}
            show_list.append(single_row)
            error_msg = ""

        no_of_results = str(cnt)

        return render(response, "home/homepage.html",
                      {'no_of_results': no_of_results, 'shows': show_list, 'error_msg': error_msg})
    else:
        print("not logged in")
        return redirect("http://127.0.0.1:8000/user/login/")


def shows(response, show_type):
    if response.session.get('is_logged_in', False) == True:

        show_list = []
        error_msg = ""
        no_of_results = ""

        if response.method == "POST":

            if response.POST.get("search_button") == 'clicked':
                print(response.POST)
                search_item = response.POST.get('search_field')
                search_item = search_item.replace(" ", "")
                search_pattern = "%" + search_item.lower() + "%"
                show_type_pattern = "%"+show_type.lower()+"%"

                print(search_pattern)
                print(show_type_pattern)

                # search_type = response.POST.get('type')
                search_genre = response.POST.get('genre')
                search_comp = response.POST.get('production')
                search_status = response.POST.get('status')
                search_lang = response.POST.get('language')

                # print(search_type)
                print(search_genre)
                print(search_comp)
                print(search_status)
                print(search_lang)


                cursor = connection.cursor()
                sql = " SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM Series se,SHOW s,ACTOR a,ACT ac" \
                      " WHERE se.SERIES_ID = s.SERIES_ID AND se.SEASON_NO = s.SEASON_NO AND" \
                      " s.SHOW_ID = ac.SHOW_IDACT AND ac.ACTOR_IDACT = a.PERSON_ID AND" \
                      " LOWER(se.CATEGORY) like (%s) AND" \
                      " regexp_replace(LOWER(a.ACTOR_FIRST_NAME || ' ' || a.ACTOR_LAST_NAME), ' ','') like (%s)" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM SERIES se,SHOW s" \
                      " WHERE s.SERIES_ID = se.SERIES_ID AND s.SEASON_NO = se.SEASON_NO AND" \
                      " LOWER(se.CATEGORY) like (%s) AND" \
                      " regexp_replace(LOWER(s.TITLE), ' ','') like (%s)" \
                      " OR regexp_replace(LOWER(s.GENRE), ' ','') like (%s)" \
                      " )" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM Series se,SHOW s,DIRECTOR d" \
                      " WHERE se.SERIES_ID = s.SERIES_ID AND se.SEASON_NO = s.SEASON_NO AND" \
                      " LOWER(se.CATEGORY) like (%s) AND" \
                      " s.DIRECTOR_ID = d.PERSON_ID" \
                      " AND regexp_replace(LOWER (d.DIRECTOR_FIRST_NAME || ' ' || d.DIRECTOR_LAST_NAME), ' ','') like (%s)" \
                      " )" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM SERIES se" \
                      " WHERE LOWER(se.CATEGORY) like (%s) AND" \
                      " regexp_replace(LOWER(se.TITLE), ' ','') like (%s)" \
                      " )"

                cursor.execute(sql, [show_type_pattern,search_pattern, show_type_pattern
                    ,search_pattern, search_pattern, show_type_pattern, search_pattern, show_type_pattern,
                                     search_pattern])
                result = cursor.fetchall();
                cursor.close()

                print(type(result))

                search_genre = response.POST.get('genre')
                search_genre = search_genre.replace(" ", "")
                search_genre = "%" + search_genre.lower() + "%"
                print(search_genre)

                search_comp = response.POST.get('production')
                search_comp = search_comp.replace(" ", "")
                search_comp = "%" + search_comp.lower() + "%"

                print(search_comp)

                search_status = response.POST.get('status')

                print(search_status)

                search_lang = response.POST.get('language')

                print(search_lang)

                result_final = []

                result_genre = []
                if search_genre != "":
                    cursor = connection.cursor()
                    sql_genre = "SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM SERIES se,SHOW s" \
                                " where se.SERIES_ID = s.SERIES_ID AND se.SEASON_NO = s.SEASON_NO AND" \
                                " LOWER(se.CATEGORY) like (%s) AND" \
                                " regexp_replace(LOWER(s.GENRE), ' ','') Like (%s)"
                    cursor.execute(sql_genre, [show_type_pattern, search_genre])
                    result_genre = cursor.fetchall()
                    cursor.close()
                else:
                    result_genre = result

                result_comp = []
                if search_comp != "":
                    cursor = connection.cursor()
                    sql_comp = "SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM SERIES se,SHOW s,PRODUCTION_COMPANY p" \
                                " where se.SERIES_ID = s.SERIES_ID AND se.SEASON_NO = s.SEASON_NO AND" \
                                " LOWER(se.CATEGORY) like (%s) AND" \
                                " s.COMPANY_ID = p.COMPANY_ID" \
                                " AND regexp_replace(LOWER(p.COMPANY_NAME), ' ','') Like (%s)"
                    cursor.execute(sql_comp, [show_type_pattern, search_comp])
                    result_comp = cursor.fetchall()
                    cursor.close()
                else:
                    result_comp = result

                result_status = []
                if search_status != "":
                    cursor = connection.cursor()
                    sql_status = "SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM SERIES se where" \
                                 " LOWER(se.CATEGORY) like (%s) AND" \
                                 " LOWER(se.STATUS) = %s"
                    cursor.execute(sql_status, [show_type_pattern, search_status.lower()])
                    result_status = cursor.fetchall()
                    cursor.close()
                else:
                    result_status = result

                result_lang = []
                if search_lang != "":
                    cursor = connection.cursor()
                    sql_lang = "SELECT DISTINCT se.SERIES_ID,se.SEASON_NO FROM SERIES se,SHOW s" \
                               " where se.SERIES_ID = s.SERIES_ID AND se.SEASON_NO = s.SEASON_NO AND" \
                               " LOWER(se.CATEGORY) like (%s) AND " \
                               " LOWER(s.LANGUAGE) = %s"
                    cursor.execute(sql_lang, [show_type_pattern, search_lang.lower()])
                    result_lang = cursor.fetchall()
                    cursor.close()
                else:
                    result_lang = result

                result_temp = set(result_genre).intersection(set(result_status).intersection(result_lang))
                result_temp_new = set(result_temp).intersection(set(result_comp))
                result_final = set(result).intersection(result_temp_new)

                error_msg = "No Result Found!"
                show_list = []

                cnt = 0
                for r in result_final:
                    cnt = cnt + 1
                    print(type(r))
                    series_id = r[0]
                    season_no = r[1]
                    cursor = connection.cursor()
                    sql = "SELECT se.SERIES_ID,se.SEASON_NO,se.TITLE,se.COVER FROM SERIES se " \
                          "WHERE se.SERIES_ID = %s and se.SEASON_NO = %s"
                    cursor.execute(sql, [series_id,season_no])
                    show_res = cursor.fetchall()
                    cursor.close()
                    print("here")

                    for r_temp in show_res:
                        show_title = r_temp[2]
                        season_no = r_temp[1]
                        show_image = r_temp[3]
                        series_id = r_temp[0]

                        cursor = connection.cursor()
                        sql = "SELECT AVG(s.IMDB_RATING) FROM SHOW s,Series se" \
                              " Where s.SERIES_ID = %s and s.SEASON_NO = %s "
                        cursor.execute(sql, [series_id, season_no])
                        res = cursor.fetchall()
                        cursor.close()

                        imdb_rating = 0
                        for r in res:
                            imdb_rating = round(r[0], 2)

                        single_row = {"show_title": show_title, "show_genre": season_no, "show_imdb": imdb_rating,
                                      "show_image": show_image}
                        show_list.append(single_row)
                        error_msg = ""
                no_of_results = str(cnt)

        else:
            cursor = connection.cursor()
            sql=""
            if show_type == "series":
                sql = "SELECT se.SERIES_ID,se.SEASON_NO,se.TITLE,se.COVER  FROM SERIES se" \
                      " where se.CATEGORY = 'TV_Series' OR se.CATEGORY = 'Mini_TV_Series'"
            if show_type == "anime":
                sql = "SELECT se.SERIES_ID,se.SEASON_NO,se.TITLE,se.COVER FROM SERIES se where se.CATEGORY = 'Anime'"

            if show_type == "documentary":
                sql = "SELECT se.SERIES_ID,se.SEASON_NO,se.TITLE,se.COVER FROM SERIES se where se.CATEGORY = 'Documentary'"

            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()


            show_list=[]
            error_msg = "No Result Found!"
            cnt = 0
            for r in result:
                cnt = cnt+1
                show_title = r[2]
                season_no = r[1]
                show_image = r[3]

                print(show_title)
                print(season_no)


                series_id = r[0]

                cursor = connection.cursor()
                sql = "SELECT AVG(s.IMDB_RATING) FROM SHOW s,Series se" \
                      " Where s.SERIES_ID = %s and s.SEASON_NO = %s "
                cursor.execute(sql, [series_id,season_no])
                res = cursor.fetchall()
                cursor.close()

                imdb_rating = 0
                for r in res:
                    imdb_rating = round(r[0], 2)

                single_row = {"show_title": show_title, "show_genre": season_no, "show_imdb": imdb_rating,
                              "show_image": show_image}
                show_list.append(single_row)
                error_msg = ""

            no_of_results = str(cnt)

        return render(response, "home/shows.html",
                  {'no_of_results': no_of_results, 'shows': show_list, 'error_msg': error_msg})



    else:
        print("not logged in")
        return redirect("http://127.0.0.1:8000/user/login/")






def movies(response):
    error_msg = ""
    no_of_results = ""
    if response.session.get('is_logged_in', False) == True:
        # return HttpResponse('This is User_ID' + request.session.get('user_ID',-1))
        id = response.session.get('user_ID', -1)
        show_list = []

        # search function
        if response.method == "POST":
            print("here")
            if response.POST.get("search_button") == "clicked":
                print(response.POST)
                search_item = response.POST.get('search_field')
                search_item = search_item.replace(" ", "")
                search_pattern = "%" + search_item.lower() + "%"

                print(search_pattern)

                # search_type = response.POST.get('type')
                search_genre = response.POST.get('genre')
                search_lang = response.POST.get('language')
                search_from = response.POST.get('from_year')
                search_to = response.POST.get('to_year')

                # print(search_type)
                print(search_genre)
                print(search_lang)
                print(search_from)
                print(search_to)

                cursor = connection.cursor()
                sql = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s,ACTOR a,ACT ac" \
                      " WHERE s.SHOW_ID = ac.SHOW_IDACT AND ac.ACTOR_IDACT = a.PERSON_ID AND" \
                      " s.SERIES_ID IS NULL AND" \
                      " regexp_replace(LOWER(a.ACTOR_FIRST_NAME || ' ' || a.ACTOR_LAST_NAME), ' ','') like (%s)" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT(s.SHOW_ID)" \
                      " FROM SHOW s, DIRECTOR d" \
                      " WHERE s.DIRECTOR_ID = d.PERSON_ID AND" \
                      " s.SERIES_ID IS NULL AND" \
                      " regexp_replace(LOWER (d.DIRECTOR_FIRST_NAME || ' ' || d.DIRECTOR_LAST_NAME), ' ','') like (%s)" \
                      " )" \
                      " UNION" \
                      " (" \
                      " SELECT DISTINCT(s.SHOW_ID) FROM SHOW s" \
                      " WHERE s.SERIES_ID IS NULL AND" \
                      " (regexp_replace(LOWER(s.TITLE), ' ','') like (%s)" \
                      " OR regexp_replace(LOWER(s.GENRE), ' ','') like (%s))" \
                      " )"

                cursor.execute(sql, [search_pattern, search_pattern, search_pattern, search_pattern])
                result = cursor.fetchall();
                cursor.close()

                print(type(result))

                search_genre = response.POST.get('genre')
                search_genre = search_genre.replace(" ", "")
                search_genre = "%" + search_genre.lower() + "%"
                print(search_genre)

                search_lang = response.POST.get('language')
                search_lang = search_lang.replace(" ", "")
                search_lang = "%" + search_lang.lower() + "%"

                print(search_lang)

                search_from = response.POST.get('from_year')

                print(search_from)

                search_to = response.POST.get('to_year')

                print(search_to)

                result_final = []

                result_genre = []
                if search_genre != "":
                    cursor = connection.cursor()
                    sql_genre = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s" \
                                " where regexp_replace(LOWER(s.GENRE), ' ','') Like (%s) AND" \
                                " s.SERIES_ID IS NULL"
                    cursor.execute(sql_genre, [search_genre])
                    result_genre = cursor.fetchall()
                    cursor.close()
                else:
                    result_genre = result

                result_lang = []
                if search_lang != "":
                    cursor = connection.cursor()
                    sql_lang = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s" \
                               " WHERE regexp_replace(LOWER(s.LANGUAGE), ' ','') Like (%s) AND" \
                               " s.SERIES_ID IS NULL"
                    cursor.execute(sql_lang, [search_lang])
                    result_lang = cursor.fetchall()
                    cursor.close()
                else:
                    result_lang = result

                result_from = []
                if search_from != "":
                    cursor = connection.cursor()
                    sql_from = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s where s.YEAR >= %s AND " \
                               " s.SERIES_ID IS NULL"
                    cursor.execute(sql_from, [search_from])
                    result_from = cursor.fetchall()
                    cursor.close()
                else:
                    result_from = result

                result_to = []
                if search_to != "":
                    cursor = connection.cursor()
                    sql_to = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s where s.YEAR <= %s AND" \
                             " s.SERIES_ID IS NULL AND"
                    cursor.execute(sql_to, [search_to])
                    result_to = cursor.fetchall()
                    cursor.close()
                else:
                    result_to = result

                result_temp = set(result_genre).intersection(set(result_from).intersection(result_to))
                result_temp_new = set(result_temp).intersection(set(result_lang))
                result_final = set(result).intersection(result_temp_new)

                error_msg = "No Result Found!"
                show_list = []

                cnt = 0
                for r in result_final:
                    cnt = cnt + 1
                    print(type(r))
                    show_id = r[0]
                    print(show_id)
                    cursor = connection.cursor()
                    sql = "SELECT * FROM SHOW WHERE SHOW_ID = %s"
                    cursor.execute(sql, [show_id])
                    show_res = cursor.fetchall()
                    cursor.close()
                    print("here")

                    for r_temp in show_res:
                        show_title = r_temp[2]
                        show_genre = r_temp[1]
                        show_des = r_temp[3]
                        show_age = r_temp[4]
                        show_lang = r_temp[8]
                        show_image = r_temp[13]
                        show_imdb = r_temp[5]
                        single_row = {"show_imdb": show_imdb,
                                      "show_title": show_title,
                                      "show_genre": show_genre,
                                      "show_des": show_des,
                                      "show_age": show_age,
                                      "show_lang": show_lang,
                                      "show_image": show_image}
                        show_list.append(single_row)
                        error_msg = ""
                no_of_results = str(cnt)

        else:
            cursor = connection.cursor()
            sql = "SELECT * FROM SHOW WHERE SERIES_ID IS NULL"
            cursor.execute(sql)
            result_show = cursor.fetchall()
            cursor.close()
            show_list = []
            cnt = 0
            for r in result_show:
                cnt = cnt + 1
                show_title = r[2]
                show_genre = r[1]
                show_imdb = r[5]
                show_image = r[13]
                single_row = {"show_title": show_title, "show_genre": show_genre, "show_imdb": show_imdb,
                              "show_image": show_image}
                show_list.append(single_row)
            no_of_results = str(cnt)
            print(no_of_results)

        return render(response, "home/movies.html",
                      {'no_of_results': no_of_results, 'shows': show_list, 'error_msg': error_msg})

    else:
        return redirect("http://127.0.0.1:8000/user/login")







