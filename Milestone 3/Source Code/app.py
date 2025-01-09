from flask import Flask, render_template, request, redirect, session
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    conn = get_db_connection()
    cursor = conn.cursor()

    if role == 'Customer':
        query = "SELECT CustomerID FROM Customer WHERE Email = ? AND Password = ?"
    elif role == 'Salesperson':
        query = "SELECT SalesPersonID FROM SalesPerson WHERE Email = ? AND Password = ?"
    elif role == 'Admin':
        query = "SELECT AdminID FROM Admin WHERE Email = ? AND Password = ?"
    else:
        return "Invalid role selected"

    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        session['role'] = role
        session['user_id'] = user[0]
        return redirect(f'/dashboard/{role.lower()}')
    else:
        return "Invalid credentials"

@app.route('/dashboard/<role>')
def dashboard(role):
    if 'role' not in session or session['role'].lower() != role:
        return redirect('/')

    if role == 'customer':
        return render_template('customer.html')
    elif role == 'salesperson':
        return render_template('salesperson.html')
    elif role == 'admin':
        return render_template('admin.html')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()

        if role == 'Customer':
            query = "INSERT INTO Customer (Name, Email, Password) VALUES (?, ?, ?)"
        elif role == 'Salesperson':
            query = "INSERT INTO SalesPerson (Name, Email, Password) VALUES (?, ?, ?)"
        elif role == 'Admin':
            query = "INSERT INTO Admin (Name, Email, Password) VALUES (?, ?, ?)"
        else:
            return "Invalid role selected"

        try:
            cursor.execute(query, (name, email, password))
            conn.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('signup.html')

@app.route('/book_car', methods=['GET', 'POST'])
def book_car():
    if 'role' not in session or session['role'].lower() != 'customer':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        car_id = request.form['car_id']
        customer_id = session['user_id']
        query = "INSERT INTO Booking (CustomerID, CarID, Status) VALUES (?, ?, 'Pending')"
        cursor.execute(query, (customer_id, car_id))
        conn.commit()
        return "Car booked successfully! <a href='/dashboard/customer'>Back to Dashboard</a>"

    # Fetch available cars
    query = "SELECT CarID, Model, Make, Price FROM Car WHERE Availability = 1"
    cursor.execute(query)
    cars = cursor.fetchall()
    return render_template('book_car.html', cars=cars)

@app.route('/book_testdrive', methods=['GET', 'POST'])
def book_testdrive():
    if 'role' not in session or session['role'].lower() != 'customer':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        car_id = request.form['car_id']
        customer_id = session['user_id']
        test_drive_date = request.form['test_drive_date']
        query = "INSERT INTO TestDrive (CustomerID, CarID, TestDriveDate) VALUES (?, ?, ?)"
        cursor.execute(query, (customer_id, car_id, test_drive_date))
        conn.commit()
        return "Test drive booked successfully! <a href='/dashboard/customer'>Back to Dashboard</a>"

    # Fetch available cars
    query = "SELECT CarID, Model, Make FROM Car WHERE Availability = 1"
    cursor.execute(query)
    cars = cursor.fetchall()
    return render_template('book_testdrive.html', cars=cars)

@app.route('/salesperson/book_car', methods=['GET', 'POST'])
def salesperson_book_car():
    if 'role' not in session or session['role'].lower() != 'salesperson':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        car_id = request.form['car_id']
        query = "INSERT INTO Booking (CustomerID, CarID, Status) VALUES (?, ?, 'Pending')"
        cursor.execute(query, (customer_id, car_id))
        conn.commit()
        return "Car booked successfully for the customer! <a href='/dashboard/salesperson'>Back to Dashboard</a>"

    # Fetch available cars and customers
    query_cars = "SELECT CarID, Model, Make FROM Car WHERE Availability = 1"
    query_customers = "SELECT CustomerID, Name FROM Customer"
    cursor.execute(query_cars)
    cars = cursor.fetchall()
    cursor.execute(query_customers)
    customers = cursor.fetchall()
    return render_template('salesperson_book_car.html', cars=cars, customers=customers)

@app.route('/salesperson/book_testdrive', methods=['GET', 'POST'])
def salesperson_book_testdrive():
    if 'role' not in session or session['role'].lower() != 'salesperson':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        car_id = request.form['car_id']
        test_drive_date = request.form['test_drive_date']
        query = "INSERT INTO TestDrive (CustomerID, CarID, TestDriveDate) VALUES (?, ?, ?)"
        cursor.execute(query, (customer_id, car_id, test_drive_date))
        conn.commit()
        return "Test drive booked successfully for the customer! <a href='/dashboard/salesperson'>Back to Dashboard</a>"

    # Fetch available cars and customers
    query_cars = "SELECT CarID, Model, Make FROM Car WHERE Availability = 1"
    query_customers = "SELECT CustomerID, Name FROM Customer"
    cursor.execute(query_cars)
    cars = cursor.fetchall()
    cursor.execute(query_customers)
    customers = cursor.fetchall()
    return render_template('salesperson_book_testdrive.html', cars=cars, customers=customers)

@app.route('/salesperson/view_bookings', methods=['GET', 'POST'])
def view_bookings():
    if 'role' not in session or session['role'].lower() != 'salesperson':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        booking_id = request.form['booking_id']
        car_id = request.form['car_id']

        # Get CustomerID from Booking
        query = "SELECT CustomerID FROM Booking WHERE BookingID = ?"
        cursor.execute(query, (booking_id,))
        customer_id = cursor.fetchone()[0]

        # Update Booking table to set status as "Approved"
        cursor.execute("UPDATE Booking SET Status = 'Approved' WHERE BookingID = ?", (booking_id,))

        # Update Car table to set availability to "No"
        cursor.execute("UPDATE Car SET Availability = 0 WHERE CarID = ?", (car_id,))

        # Add notification for the customer
        notification_message = "Your booking has been approved. Thank you for choosing us!"
        notification_query = "INSERT INTO Notification (CustomerID, Message) VALUES (?, ?)"
        cursor.execute(notification_query, (customer_id, notification_message))

        # Log the sale in the Sales table
        sale_query = """
            INSERT INTO Sales (BookingID, CarID, SaleAmount)
            SELECT ?, CarID, Price FROM Car WHERE CarID = ?
        """
        cursor.execute(sale_query, (booking_id, car_id))

        conn.commit()

    # Fetch all bookings along with car and customer details
    query = """
        SELECT b.BookingID, c.Name AS CustomerName, car.CarID, car.Model, car.Make, b.Status
        FROM Booking b
        JOIN Customer c ON b.CustomerID = c.CustomerID
        JOIN Car car ON b.CarID = car.CarID
        ORDER BY b.BookingID DESC
    """
    cursor.execute(query)
    bookings = cursor.fetchall()

    return render_template('view_bookings.html', bookings=bookings)



@app.route('/admin/manage_cars', methods=['GET', 'POST'])
def manage_cars():
    if 'role' not in session or session['role'].lower() != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form['action']
        if action == 'add':
            model = request.form['model']
            make = request.form['make']
            price = request.form['price']
            query = "INSERT INTO Car (Model, Make, Price, Availability) VALUES (?, ?, ?, 1)"
            cursor.execute(query, (model, make, price))
            conn.commit()
        elif action == 'delete':
            car_id = request.form['car_id']
            query = "DELETE FROM Car WHERE CarID = ?"
            cursor.execute(query, (car_id,))
            conn.commit()
        elif action == 'update':
            car_id = request.form['car_id']
            model = request.form['model']
            make = request.form['make']
            price = request.form['price']
            query = "UPDATE Car SET Model = ?, Make = ?, Price = ? WHERE CarID = ?"
            cursor.execute(query, (model, make, price, car_id))
            conn.commit()

    # Fetch all cars
    query = "SELECT CarID, Model, Make, Price, Availability FROM Car"
    cursor.execute(query)
    cars = cursor.fetchall()
    return render_template('manage_cars.html', cars=cars)

@app.route('/admin/manage_maintenance', methods=['GET', 'POST'])
def manage_maintenance():
    if 'role' not in session or session['role'].lower() != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        car_id = request.form['car_id']
        issue = request.form['issue']
        cost = request.form['cost']
        query = "INSERT INTO Maintenance (CarID, Issue, MaintenanceDate, Cost) VALUES (?, ?, GETDATE(), ?)"
        cursor.execute(query, (car_id, issue, cost))
        conn.commit()

    # Fetch maintenance records and cars
    query_maintenance = """
        SELECT m.MaintenanceID, c.Model, c.Make, m.Issue, m.MaintenanceDate, m.Cost
        FROM Maintenance m
        JOIN Car c ON m.CarID = c.CarID
    """
    query_cars = "SELECT CarID, Model, Make FROM Car"
    cursor.execute(query_maintenance)
    maintenance = cursor.fetchall()
    cursor.execute(query_cars)
    cars = cursor.fetchall()
    return render_template('manage_maintenance.html', maintenance=maintenance, cars=cars)

@app.route('/admin/view_reports')
def view_reports():
    if 'role' not in session or session['role'].lower() != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch sales data
    query = """
        SELECT car.Model, car.Make, COUNT(s.SaleID) AS TotalSales, SUM(s.SaleAmount) AS TotalRevenue
        FROM Sales s
        JOIN Car car ON s.CarID = car.CarID
        GROUP BY car.Model, car.Make
    """
    cursor.execute(query)
    reports = cursor.fetchall()
    return render_template('view_reports.html', reports=reports)

@app.route('/customer/submit_inquiry', methods=['GET', 'POST'])
def submit_inquiry():
    if 'role' not in session or session['role'].lower() != 'customer':
        return redirect('/')

    if request.method == 'POST':
        inquiry_text = request.form['inquiry_text']
        customer_id = session['user_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the inquiry into the database
        query = "INSERT INTO Inquiry (CustomerID, InquiryText) VALUES (?, ?)"
        cursor.execute(query, (customer_id, inquiry_text))
        conn.commit()

        return "Inquiry submitted successfully! <a href='/dashboard/customer'>Back to Dashboard</a>"

    return render_template('submit_inquiry.html')

@app.route('/salesperson/view_inquiries', methods=['GET', 'POST'])
def view_inquiries():
    if 'role' not in session or session['role'].lower() != 'salesperson':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all inquiries
    query = """
        SELECT i.InquiryID, c.Name AS CustomerName, i.InquiryText, i.Timestamp, i.Status
        FROM Inquiry i
        JOIN Customer c ON i.CustomerID = c.CustomerID
        ORDER BY i.Timestamp DESC
    """
    cursor.execute(query)
    inquiries = cursor.fetchall()

    if request.method == 'POST':
        # Handle status update
        inquiry_id = request.form['inquiry_id']
        new_status = request.form['status']

        update_query = "UPDATE Inquiry SET Status = ? WHERE InquiryID = ?"
        cursor.execute(update_query, (new_status, inquiry_id))
        conn.commit()

        return redirect('/salesperson/view_inquiries')

    return render_template('view_inquiries.html', inquiries=inquiries)

@app.route('/customer/notifications')
def customer_notifications():
    if 'role' not in session or session['role'].lower() != 'customer':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch unread notifications for the logged-in customer
    customer_id = session['user_id']
    query = "SELECT NotificationID, Message, Timestamp FROM Notification WHERE CustomerID = ? AND Status = 'Unread'"
    cursor.execute(query, (customer_id,))
    notifications = cursor.fetchall()

    # Mark notifications as "Read"
    update_query = "UPDATE Notification SET Status = 'Read' WHERE CustomerID = ? AND Status = 'Unread'"
    cursor.execute(update_query, (customer_id,))
    conn.commit()

    return render_template('notifications.html', notifications=notifications)

@app.route('/admin/generate_report', methods=['GET', 'POST'])
def generate_report():
    if 'role' not in session or session['role'].lower() != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        report_name = request.form['report_name']

        # Example: Generate Total Sales Report
        query = """
            SELECT car.Model, car.Make, COUNT(s.SaleID) AS TotalSales, SUM(s.SaleAmount) AS TotalRevenue
            FROM Sales s
            JOIN Car car ON s.CarID = car.CarID
            GROUP BY car.Model, car.Make
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Convert results to a string format
        content = "\n".join([f"Model: {row[0]}, Make: {row[1]}, Total Sales: {row[2]}, Total Revenue: ${row[3]}" for row in results])

        # Save report to the database
        insert_query = "INSERT INTO Report (ReportName, Content) VALUES (?, ?)"
        cursor.execute(insert_query, (report_name, content))
        conn.commit()

        return "Report generated and saved successfully!"

    return render_template('generate_report.html')

@app.route('/admin/view_saved_reports')
def view_saved_reports():
    if 'role' not in session or session['role'].lower() != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT ReportID, ReportName, CreatedDate FROM Report"
    cursor.execute(query)
    reports = cursor.fetchall()
    return render_template('view_saved_reports.html', reports=reports)

@app.route('/customer/search_cars', methods=['GET', 'POST'])
def search_cars():
    if 'role' not in session or session['role'].lower() != 'customer':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cars = []

    if request.method == 'POST':
        min_price = request.form['min_price']
        max_price = request.form['max_price']

        # Fetch cars within the specified price range
        query = """
            SELECT CarID, Model, Make, Price, Availability
            FROM Car
            WHERE Price BETWEEN ? AND ? AND Availability = 1
        """
        cursor.execute(query, (min_price, max_price))
        cars = cursor.fetchall()

    return render_template('search_cars.html', cars=cars)


if __name__ == '__main__':
    app.run(debug=True)
