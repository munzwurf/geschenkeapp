$(document).on("click", "input[type='radio']", function () {
    	var val_chosen = $(this).val();
    	var att_type = $(this).attr('name');
      $.ajax({
      	url: "{% url 'main:next_question' %}",
      	data: {'val_chosen':val_chosen,
      		   'att_type':att_type},
      	datatype : 'json',
      	success: function (data) {
      		if (data.last == 0) {
      			$('#question').empty();
      			$('#question').append(data.question_text);
      			var i = 0
      			data.attribute_names.forEach(function(element){
      				i++
      				$('#question').append("<div class='choice'><input type='radio' name=" + data.attribute_type_name +  " id=" + data.attribute_type_name+i +  " value=" + element.attribute_name+ " /><label>" + element.attribute_name + "</label></div>");
      				     		})
      			if (data.back == 1){
      				$('form').after("<input type='submit' value='Zurück'>");}
 
      		}
      		
      		else {
      			console.log("TRIGGER SUBMIT");
      			document.getElementById('questions').submit();
      		}
      	
      	console.log("Success");
      	}

      })
    });
 