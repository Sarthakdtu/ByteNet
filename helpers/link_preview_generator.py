import requests
from constants.secrets import LINK_PREVIEW_KEY
def get_link_preview(link):
    url = "http://api.linkpreview.net/?key=" + LINK_PREVIEW_KEY  + "&q=" + link
    res = requests.get(url).json()
    html= f"""
    <div class='' 
        style=' margin: auto;
        width: 50%;
        border: 1px solid skyblue;
        padding: 10px; 
        font-size:small;'>{res['title']} <br>
         <span style='font-size:xx-small; text-color:white;'>
         {res['description']} </span>
         <br> 
         <img src={res['image']} 
     style=' margin: auto;
        display: block;
        max-width:100%;
        max-height:100%;
        padding: 10px; 
        object-fit: contain;'> <br>
        <a href={res['url']} target='__blank' >Link to article
        <i class="fas fa-external-link-alt"></i></a>    
    </div>
    """
    return html