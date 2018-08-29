// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

// console.log("JS_handleLostConnection.js found.")
import * as notification from "/static/home/js/handleNotifications.js"

$(document).ready(function(){

    window.addEventListener('offline', function(event){
        notification.makeNotification("You are offline!", "offline")
    });

    window.addEventListener('online', function(event){
        notification.makeNotification("You are online!", "online")
        
    });

})