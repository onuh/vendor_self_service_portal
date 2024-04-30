$(function(){
	$("#wizard").steps({
        headerTag: "h4",
        bodyTag: "section",
        transitionEffect: "fade",
        enableAllSteps: true,
        transitionEffectSpeed: 500,
        onStepChanging: function (event, currentIndex, newIndex) { 
            if ( newIndex === 1 ) {
                $('.steps ul').addClass('step-2');
            } else {
                $('.steps ul').removeClass('step-2');
            }
            if ( newIndex === 2 ) {
                $('.steps ul').addClass('step-3');
            } else {
                $('.steps ul').removeClass('step-3');
            }

            if ( newIndex === 3 ) {
                $('.steps ul').addClass('step-4');
                //$('.actions ul').addClass('step-last');
            } else {
                $('.steps ul').removeClass('step-4');
                $('.actions ul').removeClass('step-last');
            }
            return true; 
        },
        labels: {
            finish: "Submit Request",
            next: "Next <i class='fa fa-arrow-right'></i>",
            previous: "<i class='fa fa-arrow-left'></i> Previous"
        }
    });
    // Custom Steps Jquery Steps
    $('.wizard > .steps li a').click(function(){
        // return // prevent direct click on steps. It must be sequential
    	$(this).parent().addClass('checked');
		$(this).parent().prevAll().addClass('checked');
		$(this).parent().nextAll().removeClass('checked');
    });
    // Custom Button Jquery Steps
    $('.forward').click(function(){
    	$("#wizard").steps('next');
    })
    $('.backward').click(function(){
        $("#wizard").steps('previous');
    })
    // Checkbox
    $('.checkbox-circle label').click(function(){
        $('.checkbox-circle label').removeClass('active');
        $(this).addClass('active');
    })

    // make the sale order field searchable select
    $('#order_id').selectize({
        sortedField: 'text'
    })

// hide and uncheck all checkboxex
 $('#report_type_many').hide();
 $('#check_forcast').prop('checked', false);
 $('.check_forcast_all').prop('checked', false);
 $('#excel_report_many').prop('checked', false);
 $('#pdf_report_many').prop('checked', false);
  var report_id = []
  var report_type;
 // select all forcast for download of report
 $('#check_forcast').click(function() {
    var inputs = document.querySelectorAll('.check_forcast_all');
        
   if(this.checked) {
    for (var i = 0; i < inputs.length; i++) {
      // console.log("Checkbox Value: "+ );
      inputs[i].checked = true;
      var intValue = parseInt(inputs[i].value)
      var rindex = report_id.indexOf(intValue)
      if(rindex > -1){
        // do nothing
      }else{
        report_id.push(intValue)
      }
      
    }
    $('#o_report_portal_generate_mass').show()
    $('#report_type_many').show()
    console.log(report_id)
   }
   else{
    for (var i = 0; i < inputs.length; i++) {
      inputs[i].checked = false;
      var intValue = parseInt(inputs[i].value)
      var rindex = report_id.indexOf(intValue)
      if(rindex > -1){
        report_id.splice(rindex, 1)
      }
    }
    $('#o_report_portal_generate_mass').hide()
    $('#excel_report_many').prop('checked', false);
    $('#pdf_report_many').prop('checked', false);
    report_type = ''
    $('#report_type_many').hide()
    console.log(report_id)
   }
 });

  $('.check_forcast_all').click(function() {

    if(this.checked) {
        $('#check_forcast').prop('checked', false);
        $('#o_report_portal_generate_mass').show()
        $('#report_type_many').show()
        var rindex = report_id.indexOf(parseInt(this.value))
        if(rindex > -1){
        // do nothing
        }else{
            report_id.push(parseInt(this.value))    
        }
    }else{
        $('#check_forcast').prop('checked', false);
        var rindex = report_id.indexOf(parseInt(this.value))
        if(rindex > -1){
            report_id.splice(rindex, 1)
        }else{
            // do nothing   
        }

        var inputs = document.querySelectorAll('.check_forcast_all');
        var is_checked = []
        for (var i = 0; i < inputs.length; i++) {

        // check if report ids array is empty
        if(report_id.length == 0){
            $('#check_forcast').prop('checked', false);
            $('#o_report_portal_generate_mass').hide()
            $('#excel_report_many').prop('checked', false);
            $('#pdf_report_many').prop('checked', false);
            $('#report_type_many').hide()
        }
    }
    }
        console.log(report_id)
 })

    $('#o_report_portal_generate_mass').click(function() {
        console.log(report_type)
        if(report_type == '' || report_type == undefined){

            alertify.error("<small style='color:#fff;'>Select One Report type.</small>");
            return
        }
        // sort array in ascending order
        report_id.sort(function(a,b){ return a - b})

        // start loader
        $("body").waitMe({effect : "ios", text : "Generating Report, Please wait...", bg : "rgba(255,255,255,0.7)", color : "#000", maxSize : "", waitTime : -1, textPos : "vertical", fontSize : "20", source : "<img src='image.jpg' />", onClose : function() {} });
         if (report_type == 'excel_report_many'){
         $.ajax({
            type: 'POST',
            url: '/my/product_forcast_report',
            xhrFields:{responseType: 'arraybuffer'},
            data: {"report_ids": JSON.stringify(report_id), "report_type": report_type},
            success: function(response, status, xmlHeaderRequest) {
                console.log(response)
                $("body").waitMe("hide")
                if(xmlHeaderRequest.getResponseHeader('Content-Type') == 'application/vnd.ms-excel'){
                    var blob = new Blob([response], {type: xmlHeaderRequest.getResponseHeader('Content-Type')})
                    var link = document.createElement('a')
                    var url = window.URL || window.webkitURL
                    link.href = url.createObjectURL(blob)
                    random = Math.floor(Math.random() * 10000)
                    link.download = 'Forcast_Report_'+random+'.xlsx'
                    link.click()

                }else{

                    var blob = new Blob([response], {type: xmlHeaderRequest.getResponseHeader('Content-Type')})
                    var link = document.createElement('a')
                    var url = window.URL || window.webkitURL
                    link.href = url.createObjectURL(blob)
                    random = Math.floor(Math.random() * 10000)
                    link.download = 'Forcast_Report_'+random+'.pdf'
                    link.click()
                }
                
            },
            error: function(xhr, status, error) {
                $("body").waitMe("hide")
                alert("Error: " + error);
            }
        });

 }else{
        $.ajax({
            type: 'POST',
            url: '/my/product_forcast_report',
            data: {"report_ids": JSON.stringify(report_id), "report_type": report_type},
            success: function(response, status, xmlHeaderRequest) {
                console.log(response)
                $("body").waitMe("hide")
                    window.open(response, '_blank')
                
            },
            error: function(xhr, status, error) {
                $("body").waitMe("hide")
                alert("Error: " + error);
            }
        });
 }

 })

  $('#excel_report_many').click(function() {
    if ($('#excel_report_many').is(':checked')) {

            report_type = 'excel_report_many'
            $('#pdf_report_many').prop('checked', false);
    }else{
        report_type = ''
        $('#pdf_report_many').prop('checked', false);
    }

 })

  $('#pdf_report_many').click(function() {

    if ($('#pdf_report_many').is(':checked')) {

            report_type = 'pdf_report_many'
            $('#excel_report_many').prop('checked', false);
    }else{

        report_type = ''
        $('#excel_report_many').prop('checked', false);
    }
 })

})
