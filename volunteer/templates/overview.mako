<%inherit file="base.mako"/>

<h2>Events ${month}-${year}</h2>

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

<%
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year +=1

    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
%>

<a href="/overview/${prev_month}/${prev_year}">Previous Month</a><a href="/overview/${next_month}/${next_year}">Next Month</a>