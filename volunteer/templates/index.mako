<%inherit file="base.mako"/>

<h1>Notification application</h1>

<h2>SMS saldo</h2>

€ ${saldo}

<h2>Upcoming events</h2>

% for event in events:
    <div class="event">
        <h3>${event.title} (${event.date}) <a href="/events/view/${event.id}">view</a></h3>
    % for slot in event.slots:
        <table>
            <thead><tr><th>${slot.team.name}</th></tr></thead>
        <tbody>
            % for user in slot.slotusers:
            <tr><td>${user.user.name}</td></tr>
            % endfor
        </tbody>
        </table>
    % endfor
    </div>
% endfor
<a href="/overview">More events</a>


<h2>Latest notifications</h2>
% for sms in smses:
    <div class="sms">
        <dl>
            <dt>To</dt><dd>${sms.to}</dd>
            <dt>Time</dt><dd>${sms.time}</dd>
            <dt>Text</dt><dd>${sms.text}</dd>
        </dl>

        % for part in sms.message_parts:
    <table>
            % for delivery in part.sms_deliveries:
                <tr>
                    <td>${delivery.scts}</td>
                    <td>${delivery.message_timestamp}</td>
                    <td>${delivery.status}</td>
                    <td>${delivery.err_code}</td>
                    <td>${delivery.to}</td>
                    <td>${delivery.network_code}</td>
                </tr>
            % endfor
    </table>
        % endfor

    </div>
% endfor



<h2>Other links</h2>
<ul>
    <li><a href='/users'>Users</a></li>
    <li><a href='/events'>Events</a></li>
    <li><a href='/teams'>Teams</a></li>
</ul>