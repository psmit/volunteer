<%inherit file="base.mako"/>
<%namespace name="forms" file="forms.mako"/>

<%block name="scripts">
<script>

</script>
</%block>

<h2>${form_title}</h2>
${forms.render_form(form)}

<p>


<table style="border: 1px black solid;" id="table-users">
    <thead><tr><th>User</th><th>Email</th><th>Phone</th><th></th></tr></thead>
<tbody>
    % for user in users:
    <tr><td>${user.name}</td><td>${user.email}</td><td>${user.nice_phone()}</td><td><a href="/users/${user.id}">edit</a></td></tr>
    % endfor

</tbody>
</table>
