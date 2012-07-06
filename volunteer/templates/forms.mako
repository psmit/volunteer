
<%def name="render_form(form, formid='form',button=True)">
    <form method="POST" action="${request.url}" id="${formid}">
        <fieldset>
            %for field in form:
                %if field.flags.hidden:
                    ${field()}
                %else:
                    <dl>
                        <dt>${field.label}</dt>
                        <dd>
                            ${field()}
                            %for error in field.errors:
                                    <span class="error">${error}</span>
                            %endfor
                        </dd>
                    </dl>
                %endif
            %endfor
            %if button:
                    <button type=submit>Submit</button>
            %endif
        </fieldset>
    </form>

</%def>