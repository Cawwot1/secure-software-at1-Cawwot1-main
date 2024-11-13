import { useCallback } from 'react';
import { useRouter } from 'next/router'; // Stage 3.1
import requestUserLogout from '../services/requestLogout';

export default function useLogout() {
  
  const router = useRouter(); // Stage 3.1

  const logout = useCallback(async () => {
    try {
      await requestUserLogout();
      console.log('User logged out successfully.'); 

      // Redirect to the login page after successful logout
      
      router.push('/login'); // Redirects to '/login' page | Stage 3.1

    } catch (error) {
      console.error('Logout failed:', error);
    }
  }, [router]);

  return logout;
}

