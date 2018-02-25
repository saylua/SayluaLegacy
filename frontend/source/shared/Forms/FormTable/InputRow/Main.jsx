import React from 'react';
import PropTypes from 'prop-types';

import { Field } from 'redux-form';


let InputRow = (props) =>  {
  const { input, label, type, placeholder, fieldId, tip, meta: { touched, error, warning } } = props;
  let id = fieldId || ('form-' + name);
  let err = touched ? error : undefined;
  let warn = touched ? warning : undefined;
  return (
    <tr>
      <td className="label">
        <label htmlFor={ id }>{ label }</label>
      </td>
      <td>
        <input {...input} id={ id } className={ err ? " error" : "" }
          placeholder={ placeholder || label } type={ type } />
        <small className={ "form-tip" + (err ? " error" : "") + (warn ? " warning" : "") }>
          { err || warn || tip }
        </small>
      </td>
    </tr>
  );
};

export default InputRow;
