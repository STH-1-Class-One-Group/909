// Supabase 클라이언트 초기화
import { supabase } from './supabase.js';

// 이메일 로그인 함수
async function login(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password
    });

    if (error) {
        throw error;
    }
    // Supabase 클라이언트가 세션을 자동으로 관리하므로 수동 쿠키 설정 제거
    // 성공 시 지도로 이동
    window.location.href = '/map';
    return data;
}

// 회원가입 함수 (플랫폼으로 로그인된 내역을 가져다가 DB-profiles에 넣음)
async function signup(email, password, nickname) {
    // 1단계: supabase Auth 회원가입
    const { data: authData, error: authError } = await supabase.auth.signUp({
        email: email,
        password: password,
        options: {
            data: { nickname: nickname } // 트리거가 사용할 닉네임 데이터 전달 (SQL Editor에 트리거 추가)
        }
    });

    if (authError) {
        throw authError;
    }
    // Supabase 클라이언트가 세션을 자동으로 관리하므로 수동 쿠키 설정 제거
    return authData;
}

// 로그아웃 함수
async function logout() {
    await supabase.auth.signOut();
    // Supabase 클라이언트가 세션을 자동으로 관리하므로 수동 쿠키 삭제 제거
    window.location.href = '/';
}

// 현재 사용자 가져오기
async function getCurrentUser() {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
}

// 구글 로그인
window.loginWithGoogle = async function() {
    try {
        const { error } = await supabaseClient.auth.signInWithOAuth({
            provider: 'google',
            options: {
                redirectTo: window.location.origin + '/map'
            }
        });

        if (error) throw error;

    } catch (error) {
        console.error('구글 로그인 에러:', error);
        alert('구글 로그인 실패: ' + error.message);
    }
}

// 카카오 로그인
window.loginWithKakao = async function() {
    console.log("🔗 카카오 로그인 버튼 클릭됨!");
    try {
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider: 'kakao',
            options: {
                redirectTo: window.location.origin + '/map' // 올바른 앱 경로로 리다이렉트
            }
        });
        if (error) throw error;
    } catch (error) {
        console.error('카카오 로그인 에러:', error.message);
        alert('카카오 로그인 실패: ' + error.message);
    }
}

// Supabase 인증 상태 변경 리스너
supabase.auth.onAuthStateChange((event, session) => {
    console.log('🔗 Auth State Change Event:', event, 'Session:', session);
    const path = window.location.pathname;
    const isPublicPath = path === '/' || path === '/signup'; // 로그인, 회원가입 페이지

    if (session) {
        console.log('✅ 로그인됨 / 세션 유지됨');
        if (isPublicPath) {
            console.log('🚀 로그인 페이지에서 /map으로 리다이렉트');
            window.location.href = '/map';
        }
    } else {
        console.log('❌ 로그아웃됨 / 세션 없음');
        // 세션이 없는데 보호된 페이지에 있으면 로그인 페이지로 이동
        if (!isPublicPath) {
            console.log('🚀 보호된 페이지에서 /로 리다이렉트');
            window.location.href = '/';
        }
    }
});

// DOMContentLoaded 이벤트 리스너는 onAuthStateChange 리스너로 대체되거나 보완될 수 있음
// 여기서는 초기 로드 시 세션 확인만 남기고, 상태 변경은 onAuthStateChange가 담당
window.addEventListener('DOMContentLoaded', async () => {
    // 초기 로드 시 세션이 있는지 확인 (onAuthStateChange가 비동기적으로 실행되기 전)
    const { data: { session } } = await supabase.auth.getSession();
    console.log('🔍 Initial DOMContentLoaded session check:', session);
    
    const path = window.location.pathname;
    const isPublicPath = path === '/' || path === '/signup';

    if (session && isPublicPath) {
        // 이미 로그인되어 있고 로그인/회원가입 페이지라면 /map으로 리다이렉트
        console.log('🚀 Initial load: Logged in on public path, redirecting to /map');
        window.location.href = '/map';
    } else if (!session && !isPublicPath && path !== '/map' && !path.startsWith('/community')) {
        // 로그인되어 있지 않고, 보호된 페이지(map, community 외)라면 로그인 페이지로 리다이렉트
        // map, community는 require_login 미들웨어에서 처리
        console.log('🚀 Initial load: Not logged in on protected path, redirecting to /');
        window.location.href = '/';
    }
});