import script_executor, llm_processor
# import data_formatter_prettier
import data_day_counter
import Sort_array_of_contacts
import logger
import Finding_markdown
# import audio_transcribe
# import credit_card_extractor
# import Finding_similar_pairs
import Extracting_sender_email
import sqlite_datamanip
import unauthorized
# import fetch_data_api
# import web_scraper
# import image_resizer


def execute_task(description):
    task_code,parameters = llm_processor.classify_task(description)
    
    if task_code == 'A1': #Completed and working
       
        output = script_executor.download_and_run_script(parameters)
        return {'task_code': task_code, 'output': output}
    

    # elif task_code == 'A2':# need to setup prettier
    #     # Suppose A2 is formatting a document
    #     output = data_formatter_prettier.format_markdown_file()
    #     return {'task_code': task_code, 'output': output}
    elif task_code == 'A3':# Done Parsing for various different days 
        
        output = data_day_counter.count_weekday(parameters)
        return {'task_code': task_code, 'output': output}
    
    elif task_code == 'A4':# Done Sorting for both last and first         
        output = Sort_array_of_contacts.sort_json(parameters)
        return {'task_code': task_code, 'output': output}
    
    elif task_code == 'A5':# Done Sorting for both last and first         
        output = logger.write_recent_logs_first_lines(parameters)
        return {'task_code': task_code, 'output': output}
    
    elif task_code == 'A6':# Done Sorting for both last and first         
        output = Finding_markdown.save_index_to_json(parameters)
        return {'task_code': task_code, 'output': output}  
     
        
    elif task_code == 'A7':# Done Sorting for both last and first         
        output = Extracting_sender_email.process_email_file(parameters)
        return {'task_code': task_code, 'output': output}    
    
    
    # elif task_code == 'A8':# Done Sorting for both last and first         
    #     output = credit_card_extractor.extract_credit_card_number(parameters)
    #     return {'task_code': task_code, 'output': output}
    
    # elif task_code == 'A9':# Done Sorting for both last and first         
    #     output = Finding_similar_pairs.find_most_similar_comments(parameters)
    #     return {'task_code': task_code, 'output': output}
    
    elif task_code == 'A10':# Done Sorting for both last and first         
        output = sqlite_datamanip.calculate_ticket_sales(parameters)
        return {'task_code': task_code, 'output': output}
    
    elif task_code == 'B1':# Done Sorting for both last and first         
        output = unauthorized.handle_b1_error()
        return {'task_code': task_code, 'output': output}
    
    elif task_code == 'B2':# Done Sorting for both last and first         
        output = unauthorized.handle_b2_error()
        return {'task_code': task_code, 'output': output}
    
    # elif task_code == 'B3':# Done Sorting for both last and first         
    #     output = fetch_data_api.fetch_and_save_data(parameters)
    #     return {'task_code': task_code, 'output': output}
    

    # elif task_code == 'B6':# Done Sorting for both last and first         
    #     output = web_scraper.scrape_website(parameters)
    #     return {'task_code': task_code, 'output': output}
    

    # elif task_code == 'B7':# Done Sorting for both last and first         
    #     output = image_resizer.process_image(parameters)
    #     return {'task_code': task_code, 'output': output}











    
    # elif task_code == 'B8':# Done Sorting for both last and first         
    #     output = audio_transcribe.transcribe_mp3_to_file(parameters)
    #     return {'task_code': task_code, 'output': output}
    

    
    else:
        return {'error': "No appropriate task found", 'task_code': task_code}
