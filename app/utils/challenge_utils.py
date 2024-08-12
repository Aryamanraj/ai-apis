def get_descriptive_participation_type(code):
    mapping = {
        "0v1": "one player daring another without participating",
        "1v1": "head-to-head challenge between two individuals",
        "NvN": "community-wide competition involving many participants"
    }
    return mapping.get(code, "unspecified competition type")

def get_descriptive_result_type(code):
    mapping = {
        "steps": "based on the total steps counted",
        "calories": "focused on calories burned",
        "validator": "requiring manual validation of submissions",
        "voting": "determined by community voting",
        "reclaim": "using digital proofs via the Reclaim protocol"
    }
    return mapping.get(code, "unspecified result determination method")