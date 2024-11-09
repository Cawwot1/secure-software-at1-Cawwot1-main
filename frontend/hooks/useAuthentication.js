import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import requestValidateToken from '../services/requestAuth';

export default function useAuthentication() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const checkAuthentication = async () => {
      const isValid = await requestValidateToken();
      if (!isValid) {
        window.location.href = "/login";
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
