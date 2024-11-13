import { useEffect, useState } from 'react';
import { useRouter } from 'next/router'; // Stage 3.1
import requestValidateToken from '../services/requestAuth';

export default function useAuthentication() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter(); // Stage 3.1

  useEffect(() => {
    const checkAuthentication = async () => {
      const isValid = await requestValidateToken();
      if (!isValid) {
        router.push('/login'); // Redirects to '/login' page | Stage 3.1
      }
      setIsAuthenticated(isValid);
    };

    checkAuthentication();

    const handleRouteChange = () => {
      checkAuthentication();
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);

  return isAuthenticated;
}
