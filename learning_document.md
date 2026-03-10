# Learning Document – Django Models & ORM Implementation

In this task, I learned the fundamentals of Django models and ORM. Django models are Python classes that represent database tables, and each field in the model represents a column in the table.

I implemented four models: Organization, JobPosting, Candidate, and Resume. I also learned how to define relationships between models using ForeignKey. For example, a JobPosting belongs to an Organization, and a Resume belongs to a Candidate and can also be linked to a JobPosting.

One important part of this task was using JSONField in the Resume model. This field is useful for storing AI-generated or AI-extracted data in JSON format. In this case, I used it to store extracted skills from resumes, such as Python, Django, SQL, and Machine Learning.

I also practiced using Django ORM to create and query data without writing raw SQL. I created sample records in the Django shell and tested queries to retrieve related objects and filter records.

Overall, this task helped me understand how Django handles database design, model relationships, migrations, admin registration, and ORM operations.

the commands i did to setup: 
cd Desktop
django-admin startproject AI_Services_Django
python manage.py startapp recruitment
