import React from 'react';
import { render } from 'react-dom';
import AAAA from './public/data.txt';

class Hello extends React.Component {

 render() {

//JSX code in return function     

  return (

       <div>

          <h1>Hello World!</h1>
          <div>{ AAAA }</div>

       </div>

    );

 }

}

render(<Hello/>, document.getElementById('app'));