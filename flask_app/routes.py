from flask import Blueprint, render_template, request
from agents.metadata_agent.metadata_agent import MetadataAgent
from agents.reference_agent.reference_agent import ReferenceAgent
from agents.image_agent.image_agent import ImageAgent
from agents.refiner_agent.refiner_agent import RefinerAgent

main_bp = Blueprint('main', __name__)

# Instantiate agents (can also use tools inside them)
metadata_agent = MetadataAgent()
reference_agent = ReferenceAgent()
image_agent = ImageAgent()
refiner_agent = RefinerAgent()

@main_bp.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        description = request.form.get("description", "")
        
        # Run agents
        metadata = metadata_agent.generate_metadata(description)
        references = reference_agent.find_references(description)
        image = image_agent.generate_image(metadata["summary"])
        
        # Refine everything
        refined = refiner_agent.refine({
            "titles": metadata["titles"],
            "summary": metadata["summary"],
            "tags": metadata["tags"],
            "references": references
        })
        
        result = {
            "metadata": metadata,
            "refined": refined,
            "image_path": image["image_path"]
        }
    
    return render_template("index.html", result=result)
