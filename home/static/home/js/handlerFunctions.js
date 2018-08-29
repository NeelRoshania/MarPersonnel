import * as notification from "./handleNotifications.js"

// Handle AJAX From Submit Success -> Update Object, handle jQuery Edit/Delete implementation
export function handleEditFormObject(data, textStatus, jqXHR){
    // console.log("handleEditFormObject - Grab object form data Success")
    // console.log(textStatus)
    // console.log(jqXHR)	// Error JSON
    // console.log("Form Data: " + data)

	// Update information div from template
	$('.editObjectForm').html(data)

	// Handle UI Interations
	$(".fa-sync").removeClass("fa-spin")
}	

// Handle AJAX From Submit Success -> Update object Object, handle jQuery Edit/Delete implementation
export function handlePaginationSuccess(data, textStatus, jqXHR){
    // console.log("handlePaginationSuccess - Pagination Success")
    // console.log(textStatus)
    // console.log(jqXHR)	// Error JSON
    // console.log(data) 

    // Handle UI Status
    $("#objectList").removeClass("blur-all")
    // console.log("handlePaginationSuccess - removed class")
    // $("#errorLog").slideUp()

	// Update information div from template
	$('#objectList').html(data)
}	  

// Handle AJAX From Submit Success -> Update object, handle jQuery Edit/Delete implementation
export function handleFormSuccess(urlLocation, refreshObject, data, textStatus, jqXHR){
    // console.log("handleFormSuccess - Form Success and Submitted")
    // console.log(urlLocation)	// Error JSON

    // Handle UI Status
    $("#objectList").removeClass("blur-all")
    // Perform ajax call to refresh template in objectList.html
    if (refreshObject) {
        // console.log("handleFormSuccess - refreshObject-> True")
        $.ajax({
            method: "GET",
            beforeSend: function(xhr) { 
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                $("#object").addClass("blur-all")
                 },
            url: urlLocation,
            success: objectRefreshSuccess,
            error: handleFormError,
        }) //Setup jQuery AJAX Call

        // Handle UI
        // alert("Form information submitted succesfully!")        
    } else {
        notification.makeNotification("Refresh page to view changes!", "standard")
        // Handle UI
        $("#objectList").removeClass("blur-all")

        // Handle UI responses
        // $("#errorLog").slideUp().empty()
        $(".fa-sync").removeClass("fa-spin")

        // $("#updateItem").append("Form submitted.")
    }

}

// Handle AJAX From Submit Success -> Update objects in objectList.html
export function objectRefreshSuccess(data, textStatus, jqXHR){
	// console.log("objectRefreshSuccess - Form Success")
	// console.log("data: " + data)

    notification.makeNotification(textStatus, "standard")
	// Update information div from template
	$('#objectList').html(data)

	// Handle UI
	$("#objectList").removeClass("blur-all")

	// Handle UI responses
    // $("#errorLog").slideUp().empty()
    $(".fa-sync").removeClass("fa-spin")

    // $("#updateItem").append("Form submitted.")
}

// Handle AJAX From Submit Failure
export function handleFormError(jqXHR, data, textStatus, errorThrown){
	// console.log("General Form Error")
    // console.log(jqXHR)
    
    // Handle UI
    $("#objectList").removeClass("blur-all")

    $(jqXHR.responseJSON["error"]).each(function(i, field){
        // console.log(field)
        notification.makeNotification(field.message, "error")
    });
}

export function handleDeleteSuccess(data, textStatus, jqXHR){
    // console.log(jqXHR)
    // console.log("data: " + data)
    notification.makeNotification(data["message"], "online")
    // Handle UI responces
    $(".fa-sync").removeClass("fa-spin")
}