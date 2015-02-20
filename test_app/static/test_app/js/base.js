$(document).ready(function () {

	Date.prototype.getData = function () {
		var dd = "" + ((this.getDate() > 9)? this.getDate(): "0" + this.getDate()),
			mm = "" + ((this.getMonth() > 9)? (this.getMonth() + 1): "0" + (this.getMonth() + 1)),
			yy = this.getFullYear();
		return [dd, mm, yy];
	}
	Date.prototype.clientFormat = function () {
		var data = this.getData(),
			dd = data[0],
			mm = data[1],
			yy = data[2];
		return dd + "." + mm + "." + yy;
	};

	Date.prototype.controlFormat = function () {
		var data = this.getData(),
			dd = data[0],
			mm = data[1],
			yy = data[2];
		return dd + "/" + mm + "/" + yy;
	};

	Date.prototype.toServerFormat = function () {
		var data = this.getData(),
			dd = data[0],
			mm = data[1],
			yy = data[2];
		return yy + "-" + mm + "-" + dd;
	}

	var add = function () {
		$("#add-form").removeClass("hide").find("input[type='submit']").click(function () {
			var parent = $("#add-form"),
				errors_stack = [],
				values = {};
			$("input[type!='submit']", parent).each(function (k, v) {
				values[$(this).attr("name")] = $(this).val();
				if ($(this).data("type") === "date") {
					values[$(this).attr("name")] = $(this).datepicker('getDate').toServerFormat();
				}
				errors_stack.push(validate.call(this));
			});
			if (errors_stack.indexOf(false) >= 0){ 
				return false;
			} else {
				$.ajax({
					"url": $("nav a.active").attr("href"),
					"data": values,
					"type": "post",
					"dataType": "json",
					"success": function (data) {
						if (data.error) {
							alert("Произошла ошибка при сохранении");
						} else {
							$("nav a.active").click();
						}
					},
					"error": function (data) {
						alert("Произошла внутренняя ошибка сервера");
					}
				})
			}
		});
	}

	var save = function () {
		if (validate.call(this)) {
			var request = {};
			request[$(this).attr("name")] = $(this).val();
			if ($(this).data('type') === "date") {
				request[$(this).attr("name")] = $(this).datepicker('getDate').toServerFormat();
			}
			$.ajax({
				"url": $("nav a.active").attr("href") + $(this).data("pk") + "/",
				"data": request,
				"type": "post",
				"dataType": "json",
				"success": function (data) {
					if (data.error) {
						alert("Произошла ошибка при сохранении");
					}
				},
				"error": function (data) {
					alert("Произошла внутренняя ошибка сервера");
				}
			})
		}
	},

	validate = function () {
		var value = $(this).val(),
			type = $(this).data("type"),
			error = true;
		// validation
		switch (type) {
			case "int":
				if (!/^\d+$/.test(value)) {
					alert('Вводимое поле может быть только числом');
					error = false;
				}
				break;
			case "char":
				if (!/^[\wа-яА-Я\s0-9]+$/.test(value)) {
					alert("Это поле должно быть заполнено только символами");
					error = false;
				}
				break;
			case "date":
				if (!/^\d{2}\/\d{2}\/\d{4}$/.test(value)) {
					alert("Дата должна быть в формате dd.mm.yyyy");
					error = false;
				}
				value = $(this).datepicker('getDate').clientFormat();
				break;
		}
		$(this).parent().find("label").html(value);
		return error;
	};

	$("nav a").click(function () {
		// строим таблицу, вешаем обработчики
		$('nav a').removeClass('active');
		$(this).addClass('active');
		$.ajax({
			'url': $(this).attr("href"),
			'dataType': 'json',
			"success": function (data) {
				var data_body = data.model_body,
					data_header = data.model_header,
					header_html = [],
					body_html = [],
					control_types = {};

				$.each(data_header, function (k, v) {
					header_html.push("<th>" +
						v.verbose_name +
					"</th>");
					control_types[v.name] = v.type;
				});

				$.each(data_body, function (k, v) {
					body_html.push("<tr>");
					// body_html.push("<td>" + v.pk + "</td>");
					control_types = control_types;
					$.each(v.fields, function (key, value) {
						if (control_types[value.name] === "date") {
							var date = new Date(value.value.split('-')),
								controlValue = date.controlFormat();
							value["value"] = date.clientFormat()
						} else {
							var controlValue = value.value;
						}
						body_html.push([
							"<td>",
								"<label for=\'", ("" + value.name) + v.pk, "\'>",
									value.value,
								"</label>",
								"<input type=\'text\' class=\'hide\' data-type=\'",
										control_types[value.name],
									"\' data-pk=\'",
										v.pk,
									"\' id=\'",
										("" + value.name) + v.pk,
									"\' name=\'",
										value.name,
									"\' value=\'",
										controlValue,
									"\'/>",
							"</td>"
						].join(""));
					});
					body_html.push("</tr>");
				});
				$("#content-block").html([
					"<table id=\"editable-table\">",
						"<tr>",
							header_html.join(""),
						"</tr>",
						body_html.join(""),
					"</table>"
				].join(""));
				
				$("#content-block")
					.append($("<a href=\'#\'>Добавить новую запись</a>").click(add));
				// Добавляем скрытую форму редактирования
				$("#content-block").append("<table id=\'add-form\' class=\'hide\'></table>");
				$.each(data_header, function (k, v) {
					if (v.name !== "id") {
						$("#add-form").append([
							"<tr>",
								"<td>",
									v.verbose_name,
								"</td>",
								"<td>",
									"<input type=\'text\'",
										"data-type=\'" + v.type + "\'",
										"id=\'" + v.name + "\'",
										"name=\'" + v.name + "\'",
										"/>",
							"</tr>"
						].join(""));
					}
				});
				$("#add-form").append("<tr><td><input type=\'submit\'/></td></tr>")

				$("#content-block #editable-table td").click(function () {
					$("label", this).addClass('hide').parent()
						.find("input")
						.removeClass("hide")
						.focusin();
				});
				$("#content-block #editable-table input").focusout(function () {
					$(this).addClass("hide").parent()
						.find("label")
						.removeClass("hide");
				}).change(save);
				$("#content-block [data-type='date']").datepicker({
					"dateFormat": "dd/mm/yy"
				});
			},
			"error": function () {
				alert('error');
			}
		});
		return false;
	});


	// что бы работал csrf
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	function sameOrigin(url) {
	    // test that a given url is a same-origin URL
	    // url could be relative or scheme relative or absolute
	    var host = document.location.host; // host + port
	    var protocol = document.location.protocol;
	    var sr_origin = '//' + host;
	    var origin = protocol + sr_origin;
	    // Allow absolute or scheme relative URLs to same origin
	    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	        // or any other URL that isn't scheme relative or absolute i.e relative.
	        !(/^(\/\/|http:|https:).*/.test(url));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	            // Send the token to same-origin, relative URLs only.
	            // Send the token only if the method warrants CSRF protection
	            // Using the CSRFToken value acquired earlier
	            xhr.setRequestHeader("X-CSRFToken", $("[name='csrfmiddlewaretoken']").val());
	        }
	    }
	});
});