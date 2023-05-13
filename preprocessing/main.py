import sys
import pandas

from utils.html_utils import HTMLUtils
from utils.text_utils import TextUtils
from utils.datetime_utils import DatetimeUtils
from database.pymongo_jobs_database import PyMongoJobsDatabase

def proceed_manually_remove_operation():
    dissertation_database = PyMongoJobsDatabase()

    print("Retrieving unprocessed job records from database.\n")
    unprocessed_job_list = dissertation_database.retrieve_unprocessed_jobs()

    total_unprocessed_job_list = len(unprocessed_job_list)
    print("Total unprocessed jobs: {}\n".format(total_unprocessed_job_list))

    if total_unprocessed_job_list == 0:
        print("No pending job records to be processed. Quit\n")
        sys.exit(0)

    # Remove job advertisements that are not related to software engineering
    for index, unprocessed_job in enumerate(unprocessed_job_list):
        print("Handling no. {} and total amount is {}\n".format(index + 1, total_unprocessed_job_list))
        id = unprocessed_job['id']
        print("Id: {}, Job title: {}, URL: {}\n".format(
            id,
            unprocessed_job['job_title'],
            unprocessed_job['url'],
        ))
        should_we_remove_it = input("Should we remove this job advertisement from database [Y/N]?\n")

        if should_we_remove_it is not None and should_we_remove_it.lower() == 'y':
            print("We are trying to delete this job advertisement from database: id = {}\n".format(id))
            has_updated = dissertation_database.mark_delete(id=id, should_delete=True)

            if has_updated:
                print("We have deleted this job advertisement from database: id = {}\n".format(id))
                unprocessed_job['has_deleted'] = True
            else:
                print("Record is already deleted! id = {}\n".format(id))
                unprocessed_job['has_deleted'] = False
        else:
            print("We will keep this record in database. id = {}\n".format(id))
            dissertation_database.mark_delete(id=id, should_delete=False)
            unprocessed_job['has_deleted'] = False

    # Remove irrelevant information from job advertisements
    for unprocessed_job in unprocessed_job_list:
        id = unprocessed_job['id']
        has_deleted = unprocessed_job['has_deleted']

        print("Id: {}, Job title: {}, URL: {}\n".format(
            id,
            unprocessed_job['job_title'],
            unprocessed_job['url'],
        ))

        if has_deleted:
            print("Record has been deleted! id = {}, Skipping this iteration.\n".format(id))
            continue
        
        print("job_description_html: {}\n".format((unprocessed_job['job_description_html'])))

        print('Any update for job_description_html? Enter `done` to stop appending to the list')
        update_for_job_description_html = input()

        job_description_html_updates = []
        while update_for_job_description_html is not None and update_for_job_description_html.lower() != 'done':
            job_description_html_updates.append(update_for_job_description_html)
            update_for_job_description_html = input()

        if len(job_description_html_updates) > 0:
            unprocessed_job['job_description_html_processed'] = ''.join(job_description_html_updates)
            print('job_description_html_processed: {}\n'.format(unprocessed_job['job_description_html_processed']))
            
            print("We are trying to update this job advertisement from database: id = {}\n".format(id))
            has_updated = dissertation_database.update_job_description_html(unprocessed_job)

            if has_updated:
                print("Job record has been updated successfully! id = {}\n".format(id))
            else:
                print("Failed to update the job record. id = {}\n".format(id))
        else:
            unprocessed_job['job_description_html_processed'] = unprocessed_job['job_description_html']
            dissertation_database.update_job_description_html(unprocessed_job)
            print("We copy the original one for this record! id = {}\n".format(id))

    print("All job advertisement records have been reviewed! See ya!\n")

def proceed_automatically_text_mining_operation():
    dissertation_database = PyMongoJobsDatabase()

    last_twelve_hours = DatetimeUtils.get_last_twelve_hours()
    print("Retrieving manually processed job records from database.\n")
    processed_manually_job_list = dissertation_database.retrieve_processed_jobs(last_updated_at=last_twelve_hours)

    total_processed_manually_job_list = len(processed_manually_job_list)
    print("Total processed manually jobs: {}\n".format(total_processed_manually_job_list))

    if total_processed_manually_job_list == 0:
        print("No pending job records to be processed. Quit\n")
        sys.exit(0)
    
    for index, processed_manually_job in enumerate(processed_manually_job_list):
        print("Handling no. {} and total amount is {}\n".format(index + 1, total_processed_manually_job_list))
        id = processed_manually_job['id']
        print("Id: {}, Source: {} and Job title: {}\n".format(
            id,
            processed_manually_job['source'],
            processed_manually_job['job_title'],
        ))

        job_description_text_to_be_updated = HTMLUtils.remove_html_tags(html=processed_manually_job['job_description_html_processed'])
        job_description_text_to_be_updated = job_description_text_to_be_updated.lower()
        job_description_text_to_be_updated = TextUtils.remove_punctuation_and_symbols(text=job_description_text_to_be_updated)
        job_description_text_to_be_updated = TextUtils.remove_stop_words(text=job_description_text_to_be_updated)
        job_description_text_to_be_updated = TextUtils.perform_lemmatization(text=job_description_text_to_be_updated)
        tokenized_job_description = TextUtils.tokenize(text=job_description_text_to_be_updated)

        processed_manually_job['job_description_text_processed'] = job_description_text_to_be_updated
        processed_manually_job['tokenized_job_description'] = tokenized_job_description

        has_updated = dissertation_database.update_job_description_text(data=processed_manually_job)

        if has_updated:
            print("Job record has been updated successfully! id = {}\n".format(id))
        else:
            print("Failed to update the job record. id = {}\n".format(id))

def proceed_generating_job_advertisements_records_operation():
    dissertation_database = PyMongoJobsDatabase()

    print("Retrieving all job advertisement records from the database\n")
    job_advertisement_records = dissertation_database.retrieve_all_jobs()
    print("Total: {}".format(len(job_advertisement_records)))

    df = pandas.DataFrame(columns=['id', 'source', 'job_title', 'job_description', 'created_at'])

    for job_advertisement in job_advertisement_records:
        job_advertisement_series_row = pandas.Series({
            'id': job_advertisement['id'],
            'source': job_advertisement['source'],
            'job_title': job_advertisement['job_title'],
            'job_description': job_advertisement['job_description_html_processed'],
            'created_at': job_advertisement['created_at'],
        }, name=job_advertisement['id'])
        df = pandas.concat([df, job_advertisement_series_row.to_frame().T])

    csv_content = df.to_csv(sep=",")
    print("Exporting all job advertisement records into a CSV file\n")
    csv_filename = './data/{}.csv'.format(DatetimeUtils.get_current_utc_time_str())
    with open(csv_filename, mode='w+') as csv_file:
        csv_file.write(csv_content)
    print("Exported to the CSV file: {}".format(csv_filename))

if __name__ == '__main__':
    print("Welcome to do the precessing\n")
    print("What kind of work do you want to proceed?\n")
    print("Enter 1 = Proceed the operation to remove information for each job advertisement record\n")
    print("Enter 2 = Proceed the operation to perform text mining handling automatically\n")
    print("Enter 3 = Proceed the operation to generate all job advertisement records into a CSV file\n")
    option = input("Your choice:\n")

    if option == '1':
        proceed_manually_remove_operation()
    elif option == '2':
        proceed_automatically_text_mining_operation()
    elif option == '3':
        proceed_generating_job_advertisements_records_operation()
    else:
        print("This application does not support this option!\n")
        sys.exit(1)
