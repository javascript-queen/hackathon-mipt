declare let GN: GN;


interface GN {
    message: string,
    user_count: number,
    users_endpoint: string,
    docs_endpoint: string,
    csrf_token: string,
    current_user: ?Record<string, any>
}
