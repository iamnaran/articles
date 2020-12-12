class UserLogoutAccess(Resource):
    """
    User Logout Api
    """

    @jwt_required
    def post(self):

        jti = get_raw_jwt()['jti']

        try:
            # Revoking access token
            revoked_token = RevokedTokenModel(jti=jti)

            revoked_token.add()

            return {'message': 'Access token has been revoked'}

        except:

            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    """
    User Logout Refresh Api
    """
    @jwt_refresh_token_required
    def post(self):

        jti = get_raw_jwt()['jti']

        try:

            revoked_token = RevokedTokenModel(jti=jti)

            revoked_token.add()

            pdb.set_trace()

            return {'message': 'Refresh token has been revoked'}

        except:

            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    """
    Token Refresh Api
    """

    @jwt_refresh_token_required
    def post(self):

        # Generating new access token
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user)

        return {'access_token': access_token}