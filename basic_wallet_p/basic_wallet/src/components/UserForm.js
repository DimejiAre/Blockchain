import React from 'react';
import { Formik, Form, Field } from 'formik';

function UserForm(props) {
    const { search } = props;

    return (
        <Formik
            initialValues={{ name: '' }}
            onSubmit={search}
            render={props => {
                return (
                    <Form>
                        <div class='userform'>
                            <label><strong>User Id:</strong></label>
                            <Field name='name' type='text' placeholder='Enter User Id' />
                            <button type="submit">Enter</button>
                        </div>
                    </Form>
                )
            }}
        />
    );
}

export default UserForm;