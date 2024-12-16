import pandas as pd
def create_film_list (category, film_category, film, actor, film_actor):
    film_list = category.merge(film_category, how = 'left', on = 'category_id', suffixes = ("_x1", "_y1"))
    film_list = film_list.merge(film, how = 'left', on = 'film_id', suffixes = ("_x2", "_y2"))
    film_list = film_list.merge(film_actor, how = 'inner', on = 'film_id', suffixes = ("_x3", "_y3"))
    film_list = film_list.merge(actor, how = 'inner', on = 'actor_id', suffixes = ("_x4", "_y4"))
    film_list['full_name'] = film_list['first_name'] + ' ' + film_list['last_name']
    film_list = film_list.groupby(['film_id', 'title', 'description', 'name', 'rental_rate', 'length', 'rating'])['full_name'].apply(lambda x: ', '.join(x))

    film_list = pd.DataFrame(film_list)
    film_list = film_list.reset_index()
    rename_column_map = {
    'film_id' : 'fid',
    'name' : 'category',
    'rental_rate' : 'price',
    'full_name' : 'actors'
    }
    
    film_list.rename(columns = rename_column_map, inplace = True)

    return film_list