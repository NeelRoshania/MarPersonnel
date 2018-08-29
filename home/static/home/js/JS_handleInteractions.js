// C:\Users\nrosh\Anaconda2\Scripts\PROJECTS\PYTHON\DJANGO\acpersonnel\ajaxified\home\js
// Ctrl D to find all of same and type to replace

// about:config -> dom.moduleScripts.enabled;true

// console.log("JS_handleInteractions.js found.")
import * as notification from "./handleNotifications.js"

$(document).ready(function(){

    // $("#toggleNotification").on("click", function() {
    //     notification.makeNotification("Lorem ipsum dolor sit amet", "standard")
    // })

    $("#notificationPanel").on("click", "#closeNotification", function(){
        $(this).closest("#notification").slideUp("fast", function(){
            $(this).remove()
        })
    })

    // HOME APP

    // Hold backgroundcolor if clicked
    $("#objectList").on("click", "#UserToDo_subject", function(){
        $(this).parent().parent().parent().toggleClass("userToDoClicked")
        $(this).closest("#UserToDo").toggleClass("margin-1em-tb")
    })

    $("#objectList").on("click", "#addUserNote_Toggle", function(){
        $(this).toggleClass("userNoteHeadingClicked")
    })

    $("#objectList").on("click", "#deleteUserToDo_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#objectList").on("click", "#deleteUserNote_Toggle", function(){
        $(this).parent().parent().parent().parent().toggleClass("deleteVis")
    })

     $("#objectList").on("click", "#deleteNoteDescription_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#objectList").on("click", "#userNote_subject", function(){
        $(this).parent().parent().parent().toggleClass("userNoteHeadingClicked")
    })

    $("#objectList").on("click", "#addNoteDescription_Toggle", function(){
        $(this).toggleClass("addNoteDescription_ToggleHover")
    })

    $(".noteDescription").on("click", "#edit", function(){
        $(this).parent().parent().parent().parent().toggleClass("noteDescriptionHover")
    })

    
    $("#searchObjectForm").on("click", "#searchHeading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })


    // PRODUCTION APP

    // Hold backgroundcolor if clicked
    $("#productionPlan").on("click", "#productionMeeting_subject", function(){
        $(this).parent().parent().parent().toggleClass("productionMeeting_clicked")
        $(this).closest("#productionList").toggleClass("margin-1em-tb")
    })

    $("#productionPlan").on("click", "#deleteProductionMeeting_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#productionPlan").on("click", "#deleteProductionNote_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#productionPlan").on("click", "#deleteRMShortage_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#productionPlan").on("click", "#deleteMaintenanceIssue_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#productionPlan").on("click", "#deleteProductionPlan_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    
    $("#productionPlan").on("click", "#productionNoteHeader", function(){
        $(this).toggleClass("productionMeetingCards_clicked")
    })

    $("#productionPlan").on("click", "#rmShortageHeader", function(){
        $(this).toggleClass("productionMeetingCards_clicked")
    })

    $("#productionPlan").on("click", "#maintenanceIssueHeader", function(){
        $(this).toggleClass("productionMeetingCards_clicked")
    })

    $("#productionPlan").on("click", "#productionPlanHeader", function(){
        $(this).toggleClass("productionMeetingCards_clicked")
    })

    $("#searchProductionForm").on("click", "#searchHeading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addProductionForm").on("click", "#insertProductionMeeting_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addProductionForm").on("click", "#insertRawMaterial_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addProductionForm").on("click", "#editRawMaterial_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addProductionForm").on("click", "#deleteRawMaterial_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })


    // SALES APP

    // Hold backgroundcolor if clicked
    $("#deliveryPlan").on("click", "#deliveryPlan_subject", function(){
        $(this).parent().parent().parent().toggleClass("deliveryPlan_clicked")
        $(this).closest("#DeliveryPlanList").toggleClass("margin-1em-tb")
    })

    $("#deliveryPlan").on("click", "#confirmDeliveryPlan_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })
    
    $("#addDeliveryRouteForm").on("click", "#deliveryPlan_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addDeliveryRouteForm").on("click", "#insertCustomerID_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addDeliveryRouteForm").on("click", "#editCustomerID_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#searchDeliveryRoutesForm").on("click", "#searchHeading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addDeliveryRouteForm").on("click", "#deleteCustomerID_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    
    // QUALITY APP

    // Hold backgroundcolor if clicked
    $("#qualityList").on("click", "#QualityObject_subject", function(){
        $(this).parent().parent().parent().toggleClass("qualityPlanHover")
        $(this).closest("#QualityPlanList").toggleClass("margin-1em-tb")
    })
    
    $("#qualityList").on("click", "#editQuality_header", function(){
        $(this).parent().toggleClass("editQualityHeader_headerClicked")
    })

    $("#qualityList").on("click", "#qualityPlan_heading1", function(){
        $(this).parent().toggleClass("qualityPlanCards_clicked")
    })

    $("#qualityList").on("click", "#qualityPlan_heading2", function(){
        $(this).parent().toggleClass("qualityPlanCards_clicked")
    })

    $("#qualityList").on("click", "#qualityPlan_heading3", function(){
        $(this).parent().toggleClass("qualityPlanCards_clicked")
    })

    $("#searchQualityList").on("click", "#searchBatchCards", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addQualityList").on("click", "#InserBatch_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addQualityList").on("click", "#RDProject_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addQualityList").on("click", "#insertProductType_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addQualityList").on("click", "#editRDProject_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addQualityList").on("click", "#editProductType_heading", function(){
        $(this).parent().parent().toggleClass("insertHeader_clicked")
    })

    $("#addQualityList").on("click", "#deleteBatchProduct_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#addQualityList").on("click", "#deleteRDProject_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })

    $("#qualityList").on("click", "#confirmUpdateQualityObject_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })
    
    $("#qualityList").on("click", "#deleteBatchProduct_Toggle", function(){
        $(this).parent().parent().parent().toggleClass("deleteVis")
    })
})