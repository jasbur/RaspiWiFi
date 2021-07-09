(function ($) {
	
	var selectedDay = "selectedDay";
	
    $.fn.weekLine = function (params) {
        if (methods[params]) {
            return methods[params].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof params === 'object' || !params) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + params + ' does not exist on jQuery.weekLine');
        }
    };

    $.fn.weekLine.defaultSettings = {
        dayLabels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        mousedownSel: true,
        startDate: null,
        onChange: null
    };

    var methods = {
        init: function (options) {
            return this.each(function () {
                var $week = $(this),
					mouseDown = false,
					weekHTML = "";
                $week.settings = 
					$.extend(true, {}, $.fn.weekLine.defaultSettings, options || {});
                $week.data("weekLine", $week.settings);

				for (i in $week.settings.dayLabels) {
					weekHTML += "<a href='#" + i + "'>" + $week.settings.dayLabels[i] + "</a>";
				}
				
                $week
					.addClass("weekDays cleanslate")
				    .append(weekHTML)
				    .mouseup(function () {
				        mouseDown = false;
				        return false;
				    });

                $days = $week.children()				    
				    .bind("mousedown", function () {
				        if ($week.settings.mousedownSel) {
							mouseDown = true;
						}
				        
						selectDay(this);
				        return false;
				    })
				    .bind("mouseenter", function () {
				        if (!mouseDown) {
							return false;
						}
						
				        selectDay(this);
				        return false;
				    });

                function selectDay(day) {
                    $(day).toggleClass(selectedDay);

                    // Check if set (because its default is null)
                    if ($.isFunction($week.settings.onChange)) {
                        $week.settings.onChange.call($week);
                    }
                }
            });
        },
        // Returns selected days in various formats
        getSelected: function (format, date) {
            var $settings = $(this).data("weekLine"),
				$prev = null,
				selected = "";

            this.children().each(function () {
                $day = $(this);

                if ($day.hasClass(selectedDay)) {
                    switch (format) {
                        case "indexes":
                            selected += $day.attr('href').substr(1) + ",";
                            break;
                        case "dates":
                            selected += 
								addDays(date ? date : 
									($settings.startDate ? $settings.startDate : new Date()),
								$day.attr('href').substr(1)) + ",";
                            break;
                        case "descriptive":
                            if ($prev == null) {
								selected = $day.html();
							}
                            else {
                                if ($day.attr('href').substr(1) - $prev.attr('href').substr(1) == 1) {
                                    var parts = 
										selected.split(',')[selected.split(',').length - 1].split('-');

                                    if (parts.length > 1) {									
                                        selected = 
											selected.replace(parts[parts.length - 1], $day.html());
									} else {
                                        selected += "-" + $day.html();
									}
                                } else {
									selected += ", " + $day.html();
								}
                            }

                            $prev = $day;
                            break;
                        case "labels":
                        default:
                            selected += $day.html() + ",";
                            break;
                    }
                }
            });

            return selected.replace(/,+$/, '');
        },
		setSelected: function (selectedDays) {
			var $this = $(this),
				$days = $this.children(),
				selDays = selectedDays.split(',');
			
			// Reset selected days
			$days.removeClass(selectedDay);
			
			for (i in selDays) {
				$days.filter(isNaN(selDays[i]) ?
					"a:contains('" + selDays[i] + "')" :
					"a:[href='#" + selDays[i] + "']").addClass(selectedDay);
			}
		}

    };

    function addDays(strDt, days) {
        var dt = new Date(strDt),
			dt = new Date(dt.setDate(dt.getDate() + Number(days))),
			d = dt.getDate(),
			m = dt.getMonth() + 1,
			y = dt.getFullYear();

        // Return d + "-" + m + "-" + y;
        return (d < 10 ? '0' + d : d) + "/" + (m < 10 ? '0' + m : m) + "/" + y;
    }

})(jQuery);

// Helper function for getting the next week day
// Monday (0) to Sunday (6)
function nextDay(dayNum) {
	return function(date) {
		var dt = new Date(date || new Date());
		return new Date(dt.getTime() + ((dayNum - dt.getDay() + 7) % 7 + 1) * 86400000);
	};
}	