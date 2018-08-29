// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

console.log("JS_Login.js found.")
import * as notification from "./handleNotifications.js"
// import * from "./handlerFunctions.js"

$(document).ready(function(){


    $(document).on('submit', '.login', function(event){
        event.preventDefault()  // Prevent the form from submitting straight away
        var $urlLocation = $(this).attr("data-url") // URL location specified in form to send data to
        var $data = $(this).serializeArray() // Grab the form information effeciently
        $(this).clear   // Clear form to prevent double submit

        // Perform ajax call to update entry
        $.ajax({
            method: "POST",
            url: $urlLocation,
            beforeSend: function(xhr) {
                notification.makeNotification("Attempting to login...", "standard") 
             },
            data: $.param($data),
            success: function(data){
                if (data["errorMessage"]) {
                    notification.makeNotification(data["errorMessage"], "error")
                } else {
                    notification.makeNotification("Login success!", "online")
                    window.location.href = data["url"];
                }
            },
            error: function(jqXHR){
                console.log(jqXHR)
                notification.makeNotification("Login error! Contact admin!", "standard")
            },     
        });
    })

})