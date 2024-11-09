import React, { useEffect, useState } from 'react';
import {
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBInput,
} from 'mdb-react-ui-kit';
import { useRouter } from 'next/router';
import styles from '../styles/Login.module.css'; // Import CSS Module
import requestUserAuthRegister from '../services/requestRegister'; // Import the request function

export const Login = () => {
    useEffect(() => {
        document.body.classList.add(styles.loginBackground);
        return () => {
          document.body.classList.remove(styles.loginBackground);
        };
    }, []);
    
    const router = useRouter(); // Initialize useRouter in the component
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState(''); 
    const [lastName, setLastName] = useState(''); 
    
    const handleSubmit = async (event) => {
        event.preventDefault(); 

        try {
          console.log('Starting registration...');
          const token = await requestUserAuthRegister(email, password, firstName, lastName);
          localStorage.setItem('authToken', token);

          window.location.href = "/forum";
        } catch (error) {
          console.error('Registration failed:', error);
          alert(`Registration failed: ${error.message}`); // Show a popup with the error message
        }
    };

    return (
        <div className={styles.loginCard}>
          <MDBCard className='text-white'>
            <MDBCardBody className='p-5 d-flex flex-column align-items-center'>
              <h2 className="fw-bold mb-2 text-uppercase">Register Account</h2>
              <p className="text-white-50 mb-5">Please enter the details below!</p>
              <form onSubmit={handleSubmit}>
                <MDBInput
                  wrapperClass='mb-4 w-100'
                  label=''
                  id='formControlLgFirstName'
                  type='text'
                  size="lg"
                  className={styles.formControl}
                  placeholder="First Name"
                  required
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                />
                <MDBInput
                  wrapperClass='mb-4 w-100'
                  label=''
                  id='formControlLgLastName'
                  type='text'
                  size="lg"
                  className={styles.formControl}
                  placeholder="Last Name"
                  required
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                />
                <MDBInput
                  wrapperClass='mb-4 w-100'
                  label=''
                  id='formControlLgEmail'
                  type='email'
                  size="lg"
                  className={styles.formControl}
                  placeholder="Email address"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <MDBInput
                  wrapperClass='mb-4 w-100'
                  label=''
                  id='formControlLgPassword'
                  type='password'
                  size="lg"
                  className={styles.formControl}
                  placeholder="Password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                
                <div className={styles.btnWrapper}>
                  <MDBBtn className={`px-5 ${styles.btn}`} size='lg' type="submit">
                    Confirm
                  </MDBBtn>
                </div>
              </form>
              <div>
                <p className="mb-0"> Have an account? 
                  <a href="login" className="text-white-50 fw-bold"> Login</a>
                </p>
              </div>
            </MDBCardBody>
          </MDBCard>
        </div>
    );
}

export default Login;
