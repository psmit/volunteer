<%inherit file="base.mako"/>
<%namespace name="forms" file="forms.mako"/>
<%block name="scripts">
<script>


    $(function() {
        //hello
        var name = $( "#name" );
        var cur_team = 'a';
        var cur_team_id = 0;
        var tips = $( ".validateTips" );

        $( "#n_form_div" ).dialog({
            autoOpen: false,
            height: 400,
            width: 350,
            modal: true,
            buttons: {
                "Add member to team": function() {

                    var dialog = $( this );

                    $.getJSON( '/teams/add_member',
                            $( '#n_form' ).serialize(),
                            function(data) {
                                if (data['success']) {
                                    $( "#team-"+cur_team_id+" tbody" ).append( "<tr>" +
                                            "<td>" + data['user_name'] + "</td>" +
                                            "</tr>" );
                                    dialog.dialog( "close" );
                                }
                                else {
                                    tips.
                                             text( data['error'] )
                                            .addClass( "ui-state-highlight" );

                                    setTimeout(function() {
                                        tips.removeClass( "ui-state-highlight");
                                    }, 500 );
                                }
                            }
                    );

                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });

        % for team in teams:
                $( "#add-user-n-${team.id}" )
                        .button()
                        .click(function() {
                            cur_team = "${team.name}";
                            cur_team_id = ${team.id};
                            //$( "#n_form_div" ).title.val("Add member to "+ cur_team +" team");
                            $( "#n_form_div" ).dialog( "option", "title", "Add member to "+ cur_team +" team" );
                            $( "#n_form_div" ).dialog( "open" );
                            $( "#team").val(cur_team_id);
                            $.getJSON( '/json/users/team/'+cur_team_id,
                                function(data) {
                                    $('#user').empty();
                                    $.each(data, function(key, v) {
                                         $('#user')
                                              .append($('<option>', { value : v[0] })
                                              .text(v[1]));
                                    })
                                }
                            );
                        });
        % endfor


        $( "#user").combobox();
    });
</script>
</%block>

<%block name="styles">
<style>
    h1 {color:#006400;}

</style>
</%block>

<h1 class="title">Teams</h1>


<table>
    % for team in teams:
        <div>
            <table style="border: 1px black solid;" id="team-${team.id}">
                <thead><tr><td>${team.name}</td></tr></thead>
                <tbody>
                % for member in team.members:
                    % if member == team.leader:
                        <tr><td style="font-weight: bold;">${member.name}</td></tr>
                    % else:
                        <tr><td>${member.name}</td></tr>
                    % endif

                % endfor

                </tbody>
            </table>
                    <button id="add-user-n-${team.id}">Add member</button>
        </div>

    % endfor
</table>

<div id="n_form_div" title="Add member to team" class="ui-widget">
${forms.render_form(form,'n_form',button=False)}

    </div>




