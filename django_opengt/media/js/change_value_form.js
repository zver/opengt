$(function() {
			$("#id_IMEI").click( function() { 
				a = $("#id_IMEI").attr("value");
				b = "Введите ID или IMEI";
				if (a == b) {
					$(this).attr("value","")
				};
			});

			$("#id_name").click( function() { 
				a = $("#id_name").attr("value");
				b = "Введите имя трекера";
				if (a == b) {
					$(this).attr("value","")
				};
			});
			
			$("#id_IMEI").blur( function() {
				b = $("#id_IMEI").attr("value");
				if (b == "") {
					$("#id_IMEI").attr("value","Введите ID или IMEI")
				}
			});
			
			$("#id_name").blur( function() {
				c = $("#id_name").attr("value");
				if (c == "") {											
					$("#id_name").attr("value","Введите имя трекера")	
				}
			});

			$("#colorpickerField2").blur( function() {
				c = $("#colorpickerField2").attr("value");
				if (c == "") {
					$("#colorpickerField2").attr("value","Выберите цвет")
				}
			});
		});