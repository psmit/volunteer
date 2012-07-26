<%inherit file="base.mako"/>
<%namespace name="forms" file="forms.mako"/>

<%block name="scripts">
    <script src="/static/jquery-ui-timepicker-addon.js"></script>
    <script>
        $(function() {
            $( "#date" ).datetimepicker({ dateFormat: "d.m.yy", timeFormat: "hh:mm" });
            $( "#start_date").datepicker({ dateFormat: "d.m.yy" });
            $( "#end_date").datepicker({ dateFormat: "d.m.yy" });
            $( "#gen_time").timepicker({timeFormat: "hh:mm"})
        });
    </script>
</%block>

<h2>${form_title}</h2>
${forms.render_form(form)}

<p>


<table style="border: 1px black solid;" id="table-events">
    <thead><tr><th>Event</th><th>Date</th><th>Theme</th><th></th><th></th></tr></thead>
    <tbody>
            % for event in events:
            <tr><td>${event.title}</td><td>${event.date}</td><td>${event.theme}</td><td><a href="/events/edit/${event.id}">edit</a></td><td><a href="/events/view/${event.id}">view</a></td></tr>
            % endfor

    </tbody>
</table>


<h3>Week generator</h3>
${forms.render_form(gen_form)}