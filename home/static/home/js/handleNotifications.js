// NOTIFICATION
    export function makeNotification(selectText, type) {
        if (type === "standard"){
            $('<div class="shadow" id="notification" style="background-color: #212121; padding: 0.8em 0em; color: white; font-style: bold !important;"><span class="my-auto col-11 col-sm-11" id="notificationText" style="font-weight: bold !important;"><span class="dropToggle" id="closeNotification"><i class="fas fa-star fa-sm" style="color: #FF1744;"></i></span><span style="padding-left: 1em;">'+selectText+'</span></span></div>').hide().appendTo("#notificationPanel").slideDown("fast").delay(2800).fadeOut("fast", function(){$(this).remove()})
        } else if (type === "online") {
            $('<div class="shadow" id="notification" style="background-color: #00E676; padding: 1em 0em; color: black; font-style: bold !important;"><span class="my-auto col-11 col-sm-11" id="notificationText" style="font-weight: bold !important;"><span class="dropToggle" id="closeNotification"><i class="fas fa-times fa-sm"></i></span><span style="padding-left: 1em;">'+selectText+'</span></span></div>').hide().appendTo("#notificationPanel").slideDown("fast")
        } else if (type === "offline") {
            $('<div class="shadow" id="notification" style="background-color: #FF3D00; padding: 1em 0em; color: white; font-style: bold !important;"><span class="my-auto col-11 col-sm-11" id="notificationText" style="font-weight: bold !important;"><span class="dropToggle" id="closeNotification"><i class="fas fa-times fa-sm"></i></span><span style="padding-left: 1em;">'+selectText+'</span></span></div>').hide().appendTo("#notificationPanel").slideDown("fast")
        } else if (type === "error") {
            $('<div class="shadow" id="notification" style="background-color: #FF3D00; padding: 1em 0em; color: white; font-style: bold !important;"><span class="my-auto col-11 col-sm-11" id="notificationText" style="font-weight: bold !important;"><span class="dropToggle" id="closeNotification"><i class="fas fa-times fa-sm"></i></span><span style="padding-left: 1em;">'+selectText+'</span></span></div>').hide().appendTo("#notificationPanel").slideDown("fast")
        } 
        
        // $("#notification").delay(2500).slideUp("fast", function(){
        //     $(this).remove()
        // }) 4500s
    }