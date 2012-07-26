<%inherit file="base.mako"/>
<%block name="scripts">
<script>
    $(function() {

        $( "#slotuser-div" ).dialog({
            autoOpen: false,
            height: 400,
            width: 350,
            modal: true,
            buttons: {
                "Add volunteer to slot": function() {

                    var dialog = $( this );

                    $.getJSON( '/slot/user/add',
                            $( '#add-slotuser-form' ).serialize(),
                            function(data) {
                                location.reload();
                            }
                    );

                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });

        % for slot in event.slots:
                $( "#slot-del-${slot.id}" )
                        .button()
                        .click(function() {
                            $.getJSON( '/slot/del',
                                    {'slot':${slot.id}},
                                    function(data) {
                                        location.reload();
                                    }
                            );
                        });
        % endfor

        $( "#add-slot" )
                .button()
                .click(function() {
                    $.getJSON( '/slot/add',
                    $( "#add-form").serialize(),
                    function(data) {
                        location.reload();
                    }
                    );
                return false;
                });

        $( ".del-slotuser")
                .button({icons: { primary: "ui-close-thick" }, text: false})
                .click(function() {
                    var parts = $(this).attr('id').split('-');
                    var slot = parts[2];
                    var user = parts[3];
                    $.getJSON( '/slot/user/del',
                            {'user':user,
                            'slot':slot},
                            function(data) {
                                location.reload();
                            }
                    );
                    return false;
                });

        $( ".add-slotuser" )
                .button()
                .click(function() {
                    var parts = $(this).attr('id').split('-');
                    var slot = parts[2];

                    $( "#slotuser-div" ).dialog( "option", "title", "Add volunteer" );
                    $( "#slotuser-div" ).dialog( "open" )
                    ;
                    $( "#slothidden").val(slot);
                    $.getJSON( '/json/users/slotevent/'+slot,
                            function(data) {
                                $('#slotuser-users').empty();
                                $.each(data, function(key, v) {
                                    $('#slotuser-users')
                                            .append($('<option>', { value : v[0] })
                                            .text(v[1]));
                                })
                            }
                    );
                });
    });
</script>
</%block>
<h2>${event.title} (${event.date})</h2>

<table>
    <thead><tr><th>Slot</th><th>Volunteers</th><th></th></tr></thead>
    <tbody>
    % for slot in event.slots:
        <tr><td>${slot.team.name}</td><td>
        <ul>
            % for slotuser in slot.slotusers:
                <li>${slotuser.user.name} <button id="del-slotuser-${slotuser.slot_id}-${slotuser.user_id}" class="del-slotuser"></button></li>
            % endfor
            </ul>
                <button id='add-slotuser-${slot.id}' class='add-slotuser'>Add</button>
        </td>
        <td>
            <button id="slot-del-${slot.id}">Delete</button>
        </td>
        </tr>
    % endfor
    </tbody>
</table>


% if len(other_teams) > 0:

<form id="add-form">
    <input type='hidden' name='event' value='${event.id}' />
    <label for='team-select'>Add slot</label>
    <select id='team-select' name='team'>
        % for t in other_teams:
        <option value=${t.id}>${t.name}</option>
        % endfor
    </select>
    <button id='add-slot'>Add</button>
</form>
% endif



<div id="slotuser-div" title="Add voluneer to slot" class="ui-widget">
    <form id="add-slotuser-form">
        <input id="slothidden" type="hidden" name="slot" value="">
        <label for='slotuser-users'>User:</label>
        <select id='slotuser-users' name='user'>

        </select>

    </form>

</div>