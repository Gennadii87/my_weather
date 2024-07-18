$(document).ready(function() {
            var lastQuery = '';
            var autocomplete = [];

            $("#city").on('input', function() {
                var query = $(this).val();

                if (query.length > 1 && query !== lastQuery) {
                    lastQuery = query;
                    $.ajax({
                        url: "autocompletion/",
                        data: {
                            q: query
                        },
                        success: function(data) {
                            autocomplete = data.autocomplete;

                            if (autocomplete.length > 0) {
                                var autocomplete = autocomplete[0];
                                var autoCompleteText = autocomplete.substring(query.length);
                                $("#city").val(query + autoCompleteText);
                                $("#city")[0].setSelectionRange(query.length, query.length + autoCompleteText.length);
                            }
                        }
                    });
                }
            });
        });