### Template agent

# Responsabilty:
#- selectiong the templetes


from app.models.state import CourseState
from app.utils.logger import log_message
from app.db.templateDB import get_all_templates, select_template_by_id

def select_template(state: CourseState) -> CourseState:

    #cheking the metadata if exested 
    metadata = state.metadata
    #cheking the metadata if exested 
    if not metadata:
        raise ValueError("Metadata must be generated before selecting a template.")

    #get the language
    language = metadata.get("language", "English")
    #get all templates
    templates = get_all_templates()
    
    selected_template_id = None
    for t in templates:
        if t.get("language", "").lower() == language.lower():
            selected_template_id = t["id"]
            break
            
    if not selected_template_id and templates:
        selected_template_id = templates[0]["id"]
        
    if not selected_template_id:
        raise ValueError("No templates found in the database.")
        
    full_template = select_template_by_id(selected_template_id)
    if not full_template:
        raise ValueError(f"Template with ID {selected_template_id} not found.")

    state.template = dict(full_template)
    
    # Log the template selection
    with log_message("TEMPLATE_AGENT", "#FF9800", f"Selected Template ID: {state.template['id']} | Description: {state.template['description']}"):
        pass

    return state