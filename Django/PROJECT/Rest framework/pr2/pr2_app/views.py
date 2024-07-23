from django.shortcuts import render,redirect
from .models import Product
from django.db import connection
# Create your views here.
def product_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Product')
        raw_products=cursor.fetchall()
        print(raw_products)
        context={'raw_products':raw_products}
        cursor.close()
        return render(request,'product_list.html',context)
    
def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']

        # Get a cursor object
        cursor = connection.cursor()

        try:       
            # Execute the query
            cursor.execute('INSERT INTO Product (name, price) VALUES (%s, %s)', [name, price])
            # Commit the transaction
            connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            connection.rollback()
            # Handle the exception or log it
            # For now, let's just print it
            print("Error:", e)
        finally:
            # Close the cursor
            cursor.close()

        # Redirect to the product list page
        return redirect('product_list')
    return render(request,'product_create.html')

def product_detail(request,product_id):
    cursor = connection.cursor()
    raw_product=()
    print(product_id,type(product_id))
    try:
        cursor.execute('SELECT * FROM Product WHERE id=%s',[product_id])
        raw_product=cursor.fetchone()

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
    print(raw_product)    
    return render(request,'product_detail.html',{'raw_product':raw_product})    

def product_delete(request,product_id):
    if request.method=='POST'
    cursor=connection.cursor()
    