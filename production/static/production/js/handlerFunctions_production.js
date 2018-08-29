import * as notification from "/static/home/js/handleNotifications.js"

// Handle AJAX From Submit Success -> Update Object, handle jQuery Edit/Delete implementation
export function handleEditFormObject_production(updateLocation, data, textStatus, jqXHR){
    // console.log("handleEditFormObject_production - Grab object form data Success")
    // console.log("Form Data: " + data)
    // console.log("updateLocation: " + updateLocation)
    
	// Update information div from template
	$('.'+ updateLocation).html(data)

	// Handle UI Interations
	$(".fa-sync").removeClass("fa-spin")
}	

// Handle AJAX From Submit Success -> Update object Object, handle jQuery Edit/Delete implementation
export function handlePaginationSuccess_production(paginationType, data, jqXHR){
    // console.log("handlePaginationSuccess_production - Pagination Success")


    // console.log("paginationType: " + paginationType)
    console.log(data) 
    if (paginationType == "RawMaterialPagination") {
        $("#rawMaterialResults").removeClass("blur-all")
        // Update information div from template
        $('#rawMaterialResults').html(data)

    } else {
        // Handle UI Status
        $("#productionPlan").removeClass("blur-all")
        // $("#errorLog").slideUp()

        // Update information div from template
        $('#productionPlan').html(data)
    } 
    
} 

// Handle AJAX From Submit Success -> Update object, handle jQuery Edit/Delete implementation
export function handleFormSuccess_production(urlLocation, refreshObject, data, textStatus, jqXHR){
    // console.log(urlLocation)	// Error JSON

    if (refreshObject) {
        // console.log("handleFormSuccess_production - refreshObject-> True")

        // Perform ajax call to refresh template in objectList.html
        $.ajax({
            method: "GET",
            beforeSend: function(xhr) { 
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                $("#productionPlan").addClass("blur-all")
                 },
            url: urlLocation,
            success: function(data) {
                objectRefreshSuccess_quality("Refresh requested!")
            },
            error: function(data, jqXHR){
                handleFormError_production(data, "Error on refreshObject", jqXHR)
            },  
        }) //Setup jQuery AJAX Call

        // Handle UI
        // alert("Form information submitted succesfully!")        
    } else {
        if (confirm("Refresh production list?")) {
            $("#refreshProductionList").trigger("click")
        } else {
            notification.makeNotification("Refresh for updates!", "standard")
        }
        
        // Handle UI Status
        $("#productionPlan").removeClass("blur-all")

        // Handle UI responses
        // $("#errorLog").slideUp().empty()
        $(".fa-sync").removeClass("fa-spin")
        // $("#updateItem").append("Form submitted.")
    }

}

// Handle AJAX From Submit Success -> Update objects in objectList.html
export function objectRefreshSuccess_production(textStatus, ajaxStatus, data, jqXHR){
    // console.log("objectRefreshSuccess_production - Form Success")

    // alert("Action complete!")
    if (ajaxStatus == "refreshProductionPlanList") {
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        $('#productionPlan').html(data)
        $("#productionPlan").removeClass("blur-all")
    } else if (ajaxStatus == "search_EDIT_RawMaterialPaginate") {
        // Handle all other search queries here
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        $('#rawMaterialResults').html(data)
        $("#rawMaterialResults").removeClass("blur-all")
        $("#productionPlan").removeClass("blur-all")
    } else {
        // Handle all other search queries here
        // console.log("refresh ajaxStatus: " + ajaxStatus)
        $('#productionPlan').html(data)
        $("#productionPlan").removeClass("blur-all")
    }

    notification.makeNotification(textStatus, "standard")
    // Handle UI responses
    // $("#errorLog").slideUp().empty()
    $(".fa-sync").removeClass("fa-spin")
}

// Handle AJAX From Submit Failure
export function handleFormError_production(errorLocation, jqXHR){
	// console.log("General Form Error")
    // console.log(jqXHR)
    
    // Handle UI
    $("#productionPlan").removeClass("blur-all")
}

export function handleDeleteSuccess_production(data, textStatus, jqXHR){
    // console.log(jqXHR)
    // console.log("data: " + data)

    // Handle UI responces
    $(".fa-sync").removeClass("fa-spin")
}