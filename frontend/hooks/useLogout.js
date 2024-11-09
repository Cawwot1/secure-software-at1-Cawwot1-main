import { useCallback } from 'react';
import { useRouter } from 'next/router';
import requestUserLogout from '../services/requestLogout';

export default function useLogout() {
  const router = useRouter();

  const logout = useCallback(async () => {
    try {
      await requestUserLogout();
      console.log('User logged out successfully.');

      // Redirect to the login page after successful logout
      window.location.href = "/login";
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }, [router]);

  return logout;
}

